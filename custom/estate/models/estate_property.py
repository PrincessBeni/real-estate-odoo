from dateutil import relativedelta
from odoo import api, fields, models


class Estate(models.Model):
    _name = 'estate.estate'
    _description = 'real estate'

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
    garden_area = fields.Integer(string='Garden Area')

    state = fields.Selection(string='State', required=True,
                             selection=[('new_state', 'New'), ('offer_received', 'Offer Received'),
                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                        ('canceled', 'Canceled')], copy=False, default='new_state')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')])
    active = fields.Boolean(string='Active', default=True)
    # state = fields.Selection([('new_state', 'New'), ('offer_received', 'Offer Received'),
    #                           ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
    #                          required=True, default='New', copy=False)

    # # state = fields.Selection(string='state',
    #                          selection=[('new_state', 'New'), ('offer_received', 'Offer Received'),
    #                                                     ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
    #                                                     ('canceled', 'Canceled')])
    property_description = fields.Text(string='Property Description')
    buyer = fields.Many2one('res.users', string='Buyer', copy=False)
    salesperson = fields.Many2one(comodel_name='res.partner', string='Sales Person', required=False,
                                  default=lambda self: self.env.user)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id',
                                required=False)


# one2many code. This class is linked to the estate_property_type_class
# class EstateLine(models.Model):
#     _name = 'estate.line'
#
#     product_id = fields.Many2one('product.product', string='Product')
#     estate_id = fields.Many2one('estate.property.type')
#     price = fields.Float(string='Price', required=False)
