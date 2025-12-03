{
    'name': 'iwesabe quality custom',
    'version': '19.0.1.0.0',
    'category': 'quality',
    'author': '',
    'depends': ['quality_control','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/quality_views.xml',
        'views/branch_screen_view.xml',
        'views/franchise_screen_views.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}
