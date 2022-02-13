# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    new_test_field = fields.Char(string='new_test_field')