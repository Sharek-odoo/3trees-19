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
    'name': 'iWesabe Account Branch Report Enterprise',
    'version': '19.0.0.1',
    'category': '',
    'description': """Branch Report
    """,
    'author': 'iWesabe',
    'website': 'https://www.iwesabe.com',
    "depends": [
        'account',
        'account_accountant',
        'account_reports',
        'iwesabe_branch_management',
        'iwesabe_branch_account'
    ],
    "data": [
        # 'views/template_view.xml',
        'data/balance_sheet.xml',
        'views/account_report_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'iwesabe_branch_report_enterprise/static/src/js/custom_account_reports.js'
'iwesabe_branch_report_enterprise/static/src/components/branch_report/filters.js'
        ],

    },
    'license': 'AGPL-3',
    'installable': True,
}
