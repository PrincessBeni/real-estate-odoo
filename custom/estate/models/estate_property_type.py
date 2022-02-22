from dateutil import relativedelta
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'type of estate property'

    # Add the Real Estate Property Type table

    type_name = fields.Char(string='Property Name', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    property_type_id = fields.Many2one('account.account', string='Property Type')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False,
                                    default=lambda self: fields.Datetime.now() + relativedelta.relativedelta(months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    salesperson = fields.Many2one('res.partner', string='Sales Person', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.users', string='Buyer', copy=False)
    property_description = fields.Text(string='Property Description')
    # hey = fields.Char(string='Hey', required=True, translate=True)

    # estate_lines_ids = fields.One2many('estate.line', 'estate_id')
