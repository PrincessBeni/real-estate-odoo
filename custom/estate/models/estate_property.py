from dateutil import relativedelta
from odoo import api, fields, models

from odoo.exceptions import MissingError, UserError, ValidationError, AccessError


class Estate(models.Model):
    _name = 'estate.estate'
    _description = 'real estate'
    _order = 'id desc'

    # The selling price should be read - only(it will be automatically filled in later)
    # The availability date and the selling price should not be copied when duplicating a record
    # The default number of bedrooms should be 2
    # The default availability date should be in 3 months

    name = fields.Char(string='Property Name', required=True, translate=True)
    postcode = fields.Char(string='Postcode')

    # Add specific number of days
    # date_availability = fields.Date(string='Date Availability', copy=False,
    #                               default=lambda self: fields.Datetime.now()+timedelta(days=30))

    # Another way to add specific number of days
    date_availability = fields.Date(string='Date Availability', copy=False,
                                    default=lambda self: fields.Datetime.now() + relativedelta.relativedelta(days=10))

    date_availability = fields.Date(string='Available From', copy=False,
                                    default=lambda self: fields.Datetime.now() + relativedelta.relativedelta(months=3))
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string='Tags')
    no_bedrooms = fields.Integer(string='No. of Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area(sqm)')

    state = fields.Selection(string='State', required=True,
                             selection=[('new_state', 'New'), ('offer_received', 'Offer Received'),
                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                        ('canceled', 'Canceled')], copy=False, default='new_state')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')])
    active = fields.Boolean(string='Active', default=True)
    property_description = fields.Text(string='Property Description')
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one(comodel_name='res.users', string="Sales Person", index=True, default=lambda self: self.env.user)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id',
                                required=False)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', required=False)
    total_area = fields.Integer(compute="_compute_total_area", string='Total area', required=False)

    # Compute the total area by adding living_area and garden_area
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    best_price = fields.Float(compute="_compute_best_price", string='Best Price', required=False)

    # Add the following constraints to their corresponding models:
    # A property expected price must be strictly positive

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',
         'The expected price of a property must be a positive number.')
    ]

    # The selling price of a property must be strictly positive
    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price of a property must be a positive number.')
    ]

    # A type name must be unique
    _sql_constraints = [('name',
                         'UNIQUE (name)',
                         'Property name already exists'), ]

    # Add a constraint so that the selling price cannot be lower than 90% of the expected price.
    @api.onchange("selling_price', 'expected_price")
    @api.constrains('selling_price', 'expected_price')
    def _check_percent(self):
        if self.selling_price:
            for offer in self:
                if offer.selling_price < (0.9 * offer.expected_price):
                    raise ValidationError('Selling price can not be less than 90% of the expected price.')

    # Compute the best price that was offered and display it in the best_price field
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for p in self:
            p.best_price = 0
            if p.mapped('offer_ids.price'):
                p.best_price = max(p.mapped('offer_ids.price'))
            else:
                p.best_price = 0

    # Set values for garden area and orientation.
    # Create an onchange to set values for the garden area (10) and orientation
    # (North) when garden is set to True.When unset, clear the fields.
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    # Cancel and set a property as sold.
    # Add the buttons ‘Cancel’ and ‘Sold.’
    # A canceled property cannot be set as sold, and a sold property cannot be canceled.
    def action_sold(self):
        for pty in self:
            if pty.state == 'canceled':
                raise UserError('Canceled properties can not be sold')
            else:
                pty.state = 'sold'
        return True

    def action_cancelled(self):
        for pty in self:
            if pty.state == 'sold':
                raise UserError('Sold properties can not be Canceled')
            else:
                pty.state = "canceled"
        return True

    # Prevent deletion of a property if its state is not ‘New’ or ‘Canceled’
    @api.ondelete(at_uninstall=False)
    def _unlink_except_installed(self):
        for p_state in self:
            if p_state.state in ('offer_received', 'offer_accepted', 'sold'):
                raise UserError('You can not delete properties that are not new or canceled.')



