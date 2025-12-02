# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Customer RFQ Portal",
    "author": "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "summary": "Request Quotation Portal, Request For Quotation Portal, RFQ at Portal, Customer Website portal, Website Portal for Purchases, Quotation Portal, Customer Portal, Client Portal, Vendor Portal, Portal Quotation  Odoo",
    "description": """This module helps customers to send a request for the quotation at the portal. They can create a quotation with single or multiple products with product quantity, invoice & shipping address. Customers can add notes in the quotation at the portal.""",
    "version": "16.0.2",
    "depends": [
        "sale_management",
        "website"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sh_customer_rfq_portal_template.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'sh_customer_rfq_portal/static/src/js/sh_customer_rfq_portal.js',
        ],
    },
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": "50",
    "currency": "EUR"
}
