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

from odoo import api, fields, models


class AccountAsset(models.Model):

    _inherit = 'account.asset'

    @api.model
    def _get_asset_default_branch(self):
        user_obj = self.env['res.users']
        branch_id = user_obj.browse(self.env.uid).branch_id.id or False
        return branch_id

    branch_id = fields.Many2one(
        'res.branch',
        'Branch',
        required=True,
        default=_get_asset_default_branch
    )
