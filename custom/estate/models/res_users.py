from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='estate.estate',
        inverse_name='user_id',
        string='Property',
        required=False)
