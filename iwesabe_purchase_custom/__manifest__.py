{
    'name': 'iwesabe_purchase_custom',
    'version': '19.0.1.0.0',
    'category': 'purchase',
    'summary': 'This apps help to define a discount per line in the purchase orders.',
    'author': '',
    'depends': ['base','purchase','purchase_stock'],
    'data': [
            'views/purchase.xml',
            'views/res_config_setting_view.xml',
            # 'views/inherit_purchase_report.xml'
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}