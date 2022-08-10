from datetime import timedelta

from odoo import api, fields, models
from odoo.odoo.exceptions import UserError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    short_name = fields.Char('Short Title', required=True)
    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
        'State', default="draft")
    description = fields.Html('Description', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner',
                                  string='Authors')
    image = fields.Binary(attachment=True)
    html_description = fields.Html()
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer('Number of Pages', groups='base.group_user',
                           states={'lost': [('readonly', True)]},
                           help='Total book page count', company_dependent=False)
    reader_rating = fields.Float(
        'Reader Average Rating',
        digits=(14, 4),  # Optional precision decimals,
    )
    currency_id = fields.Many2one(
        'res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price',
    )
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    publisher_city = fields.Char(
        string='Publisher City',
        related='publisher_id.city',
        readonly=True)
    category_id = fields.Many2one('library.book.category')
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,  # optional
        compute_sudo=True  # optional
    )
    # Reference fields are similar to many-to-one fields, except that they allow the user to select
    # the model to link to.
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)',
         'Book title must be unique.'),
        ('positive_page', 'CHECK(pages >= 0)',
         'No of pages must be positive')
    ]

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))
        return result

    def book_rent(self):
        self.ensure_one()
        if self.state != 'available':
            raise UserError('Book is not available forrenting')
            rent_as_superuser = self.env['library.book.rent'].sudo()
            rent_as_superuser.create({
                'book_id': self.id,
                'borrower_id': self.env.user.partner_id.id,
            })

    # Prevent release dates in the future.
    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError(
                    'Release date must be in the past')

    # Calculate the days since the book's release date
    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for days in self:
            if days.date_release:
                total = today - days.date_release
                days.age_days = total.days
            else:
                days.age_days = 0

    # Write on the computed field
    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

# If you use store=True in your compute field, you no longer need to
# implement the search method because the field is stored in a database and you can
# search/sort based on the stored field.
# Search in the computed field
    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]