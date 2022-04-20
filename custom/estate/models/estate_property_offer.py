import datetime

from odoo import api, fields, models, tools
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers for our real estate properties'
    _order = 'price desc'

    price = fields.Float(string='Price', required=False)
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused'), ],
                              required=False, copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.estate', required=True)

    validity = fields.Integer("Offer Validity", default=7)
    deadline_date = fields.Date(string='Deadline', compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    property_type_id = fields.Many2one(related='property_id.property_type_id', string='PropertyType', store=True)

    # An offer price must be strictly positive
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'The price of an offer must be a positive number.')
    ]

    @api.depends("validity")
    def _compute_deadline_date(self):
        for duration in self:
            if duration.create_date:
                duration.deadline_date = duration.create_date + datetime.timedelta(days=duration.validity)

    def _inverse_deadline_date(self):
        for duration in self:
            if duration.deadline_date:
                duration.validity = (duration.deadline_date - duration.create_date.date()).days

    # Add the buttons Accept and Refuse
    # When an offer is accepted, set the buyer and the selling price for the corresponding property.
    @api.depends('property_id.selling_price, property_id.buyer,property_id.state')
    def action_accept(self):
        for pty in self:
            pty.status = 'accepted'
            pty.property_id.state = 'offer_accepted'
            pty.property_id.selling_price = pty.price
            pty.property_id.buyer = pty.partner_id
        return True

    def action_refuse(self):
        for pty in self:
            pty.status = 'refused'
        return True

    # At offer creation, set the property state to ‘Offer Received’.
    # Also raise an error if the user tries to create an offer with a lower amount than an existing offer.
    @api.model
    def create(self, vals):
        prop_id = self.env['estate.estate'].browse(vals['property_id'])
        print(prop_id.state)
        if tools.float_compare(prop_id.best_price, vals['price'], precision_digits=3) >= 0:
            raise ValidationError('You are trying to create an offer with a price lower than an existing offer(s).')
        prop_id.state = 'offer_received'
        return super(EstatePropertyOffer, self).create(vals)
