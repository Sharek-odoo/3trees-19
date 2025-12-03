{
    'name': 'MRP Loss And NET Qty',
    'version': '1.4',
    'summary': 'Adds Loss % and Net Quantity fields to BOM Order Line And Manufacturing Order Line.',
    'description': 'A simple module to add custom fields (Loss % and Net Quantity) to the BOM Order Line screen in the Manufacturing module.',
    'author': 'iwesabe',
    'website': 'https://www.iwesabe.com',
    'category': 'Manufacturing',
    'depends': ['mrp'],
    'data': [
        'views/mrp_bom_line_views.xml',
        'views/mrp_production_line.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}



