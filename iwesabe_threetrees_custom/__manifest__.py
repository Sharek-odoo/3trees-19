# -*- coding: utf-8 -*-
{
    'name': 'Iwesabe Threetrees Custom',
    'category': 'Inventory/Purchase',
    'version': '1.4',
    'description': 'send mail when delivery confirm',
    'author': '',    
    'depends': ['sale_management', 'fleet', 'account', 'stock', 'purchase'],
    'data': [
        'data/ir_sequence_data.xml',
        'data/reordering_rfq_mail.xml',
        'views/account_move_views.xml',
        'views/fleet_vehicle_odometer_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
        'views/report_invoice.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}
