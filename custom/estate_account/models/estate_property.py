from odoo import api, fields, models


class InheritedEstateProperty(models.Model):
    _inherit = 'estate.estate'

    # Create an empty account.move in the override of the action_sold method:
    # The partner_id is taken from the current estate.property
    # The move_type should correspond to a ‘Customer Invoice’
    # The journal_id must be a sale journal

    # Add two invoice lines during the creation of the account.move.
    # Each property sold will be invoiced following these conditions:
    # 6 % of the selling price
    # An additional 100.00 from administrative fees
    def action_sold(self):
        partner = super().action_sold()
        if partner:
            journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
            self.env['account.move'].create({
                'partner_id': self.buyer,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06
                    }),
                    (0, 0, {
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            })
        return partner
