from dateutil import relativedelta
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'type of estate property'
    _order = 'name'

    name = fields.Char(string='Property Name', required=True, translate=True)
    property_ids = fields.One2many(comodel_name='estate.estate', inverse_name='property_type_id', required=False)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id',
                                required=False)
    offer_count = fields.Integer(compute="_compute_offer_count", string='Offers', required=False)

    # Count the number of property offers
    @api.depends('offer_ids.property_type_id')
    def _compute_offer_count(self):
        for offer in self:
            offer.offer_count = 0
            if offer.mapped('offer_ids.property_type_id'):
                offer.offer_count = self.env['estate.estate'].search_count([('property_type_id', '=', offer.id)])
            else:
                offer.offer_count = 0

# This is one2many code. It is linked to the estate_line class defined in the estate_property class
# estate_lines_ids = fields.One2many('estate.line', 'estate_id')
