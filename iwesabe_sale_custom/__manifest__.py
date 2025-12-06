# -*- coding: utf-8 -*-
{
    'name': 'Sale Custom',
    'category': 'Sales',
    'version': '19.0',
    'description': 'Sales custom',
    'author': '',
    'depends': ['base', 'sale_management', 'stock', 'account'],
    'data': [
        'data/mail_template.xml',
        'views/data.xml',
        'views/stock_warehouse_view.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}
