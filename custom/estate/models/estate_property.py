# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EstateProperty(models.Model):
    _name = 'estate.estate'
    _description = 'real estate'

    name = fields.Char(string='Title', required=True, translate=True)
    property_type = fields.Integer(string='#Property Type', required=True)
    postcode = fields.Char(string='Postcode', required=True)
    date_availability = fields.Date(string='Date Availability')
    tags = fields.Char(string='Tags', translate=True)
    no_bedrooms = fields.Integer(string='No. of Bedrooms')
    living_area = fields.Integer(string='Living Area (sqm)')
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('North', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')])




    # @api.depends('value')

    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100



# name = fields.Char('Plan Name', required=True, translate=True)
# number_of_months = fields.Integer('# Months', required=True)
# active = fields.Boolean('Active', default=True)
# sequence = fields.Integer('Sequence', default=10)
#
# _sql_constraints = [
#     ('check_number_of_months', 'CHECK(number_of_months >= 0)', 'The number of month can\'t be negative.'),
# ]
