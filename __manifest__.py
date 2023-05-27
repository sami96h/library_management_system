{
    'name': 'library management',
    'version': '1.0',
    'summary': 'Track leads and close opportunities',
    'description': "",
    'category': 'Library Management',
    'depends': [
    ],
    'data': [

        'security/library_management_security.xml',
        'security/ir.model.access.csv',
        'views/library_author_views.xml',
        'views/library_reservation_views.xml',
        'views/library_book_views.xml',
        'wizard/update_book_price_wizard_view.xml',
        'views/library_management_menus.xml',
        'report/book_report.xml',
        'views/library_book_copy.xml'
    ],
    'demo': [
    ],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False
}