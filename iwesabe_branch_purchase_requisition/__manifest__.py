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
    'name': 'iWesabe Purchase Requisition Branch',
    'description': """
        Branch in Purchase Requisition
    """,
    'version': '19.0.0.1',
    'author': 'iWesabe',
    'category': 'purchase',
    'website': 'https://www.iwesabe.com',
    'depends': ['iwesabe_branch_management','purchase_requisition'],
    'data': [
        'security/security.xml',
        'views/purchase_requisition_view.xml'
    ],
    'license': 'AGPL-3',
    'installable': True,
}
