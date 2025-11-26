# * coding: utf8 *
##############################################################################
#
#    Global Creative Concepts Tech Co Ltd.
#    Copyright (C) 2018TODAY iWesabe (<http://www.iwesabe.com>).
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'iWesabe Stock Branch',
    'version': '19.0.0.1',
    'category': '',
    'description': """
        Branch in Stock/Location/Warehouse
    """,
    'author': 'iWesabe',
    'website': 'https://www.iwesabe.com',
    'depends': ['iwesabe_branch_management', 'stock', 'stock_account'],
    'data': [
        'security/security.xml',
        'views/stock_warehouse_view.xml',
        'views/stock_location_view.xml',
        'views/stock_picking.xml',
        'views/stock_move.xml',
        'views/stock_scrap_view.xml',
        'views/quant_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
}
