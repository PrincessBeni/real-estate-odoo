from odoo import api, fields, models, _


class BookCategory(models.Model):
    _name = 'library.book.category'
    _parent_store = True
    _parent_name = "main_parent_id"  # optional if field is only 'parent_id'
    parent_path = fields.Char(index=True)

    name = fields.Char('Category')
    main_parent_id = fields.Many2one(
        'library.book.category',
        string='Parent Category',
        ondelete='restrict',
        index=True)
    child_ids = fields.One2many(
        'library.book.category', 'main_parent_id',
        string='Child Categories')

    @api.constrains('main_parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
                'Error! You cannot create recursive categories.'
            )
