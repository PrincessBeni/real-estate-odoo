from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    published_book_ids = fields.One2many(
        'library.book', 'publisher_id',
        string='Published Books')

    authored_book_ids = fields.Many2many(
        'library.book',
        string='Authored Books',
        # relation='library_book_res_partner_rel'
        # optional
    )
