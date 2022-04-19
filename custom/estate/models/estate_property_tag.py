from odoo import api, fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags for estate property'
    _order = 'name'

    name = fields.Char(string='Tag Name', required=False)
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color', required=False)
    # tag_ids = fields.Many2many(comodel_name='estate.estate', string='Tags')

    # A property tag name must be unique
    _sql_constraints = [('name',
                         'UNIQUE (name)',
                         'This property tag already exists'), ]
