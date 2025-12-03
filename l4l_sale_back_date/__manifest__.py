# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

{
    'name': 'Sale Back Date',
    'category': 'Sales/Sales',
    'version': '19.0.1.0',
    'sequence': 5,
    'summary': 'BackDate in Sale Order, Set BackDate in Sale, Stock, Sale, Sale Order, Purchase, Purchase Order, Inventory, Transfer, Invoice',
    'description': "This Module Allows Users to Easily Backdate Transactions from the Sale Order, Overcoming the Standard Odoo limitation. By Modifying the Order Date During Confirmation, This Module Ensures that Associated Documents, such as Delivery Schedules and Accounting Journal Entries, Reflect the Selected Date Accurately, Streamlining Transaction Timelines in Odoo.",
    'author': 'Leap4Logic Solutions Private Limited',
    'website': 'https://leap4logic.com/',
    'depends': ['sale_management', 'stock', 'sale_stock'],
    'data': [
        'views/res_config_views.xml',
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    "price": 11.99,
    "currency": "USD",
    "live_test_url": 'https://youtu.be/IY-RsQF_daQ',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
