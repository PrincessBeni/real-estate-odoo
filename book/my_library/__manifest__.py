# -*- coding: utf-8 -*-
{
    'name': "My Library",

    'summary': """
        Manage books easily""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/library_book_categ.xml',
        'views/res_partner.xml',
        'views/library_book.xml',
        'views/templates.xml',
        'views/library_book_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/my_library/static/src/css/my_library.css',
            '/my_library/static/src/scss/my_library.scss',
            '/my_library/static/src/js/my_library.js',
        ],
    },
}
