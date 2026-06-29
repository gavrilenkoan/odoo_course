# noinspection PyStatementEffect
{
    'name': 'Library',
    'summary': '',
    'author': 'Odoo School',
    'website': 'https://odoo.school/',
    'category': 'Customization',
    'license': 'OPL-1',
    'version': '19.0.1.0.0',

    'depends': [
        'base',
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/library_menu.xml',
        'views/library_book_views.xml',
    ],
    
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/library.book.csv',
    ],

    'images': [
        'static/description/icon.png',
    ],

    'installable': True,
    'auto_install': False,
}