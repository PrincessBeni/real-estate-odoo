from odoo import api, fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags for estate property'

    name = fields.Char(string='Tag Name', required=False)
    active = fields.Boolean(string='Active', default=True)
    # tag_ids = fields.Many2many(comodel_name='estate.estate', string='Tags')
