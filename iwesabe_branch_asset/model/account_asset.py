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

from odoo import api, fields, models, _
from odoo.exceptions import UserError 


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    branch_id = fields.Many2one('res.branch', 'Branch')

    def compute_depreciation_board(self):
        res = super(AccountAsset, self).compute_depreciation_board()
        if self.depreciation_move_ids:
            self.depreciation_move_ids.write({
                'branch_id': self.branch_id and self.branch_id.id or False
            })
            self.depreciation_move_ids.mapped('line_ids').write({
                'branch_id': self.branch_id and self.branch_id.id or False
            })
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _auto_create_asset(self):
        res = super(AccountMove, self)._auto_create_asset()
        if res:
            res.update({
                'branch_id': self.branch_id and self.branch_id.id or False
            })
        return res
