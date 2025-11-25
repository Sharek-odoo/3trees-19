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


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _get_default_branch(self):
        user = self.env['res.users']
        print("UserID >>>>>>", self.env.uid)
        return user.browse(self.env.uid).branch_id.id or False

    def _get_allowed_branches(self):
        branches = self.env.user.branch_ids
        print("Allowed Branches >>>>> ", branches)
        return [('id', 'in', branches.ids)]

    branch_id = fields.Many2one(
        'res.branch',
        'Branch',
        default=_get_default_branch,
        domain=_get_allowed_branches
    )

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        if not res.branch_id:
            if hasattr(res, 'stock_move_id') and res.stock_move_id:
                res.branch_id = res.stock_move_id.branch_id
        return res

    def _post(self, soft=True):
        res = super(AccountMove, self)._post(soft=soft)
        for move in self:
            if move.branch_id and not move.line_ids.branch_id:
                move.mapped('line_ids').write({
                    'branch_id': move.branch_id and move.branch_id.id or False
                })
        return res

    @api.onchange('purchase_vendor_bill_id', 'purchase_id')
    def _onchange_purchase_auto_complete(self):
        if self.purchase_vendor_bill_id.vendor_bill_id:
            self.branch_id = self.purchase_vendor_bill_id.vendor_bill_id.branch_id
        elif self.purchase_vendor_bill_id.purchase_order_id:
            self.branch_id = self.purchase_vendor_bill_id.purchase_order_id.branch_id
            ctx = dict(self.env.context)
            ctx.update({
                'perfect_purchase_vendor_bill_id': self.purchase_vendor_bill_id
            })
            self.env.context = ctx
        res = super(AccountMove, self)._onchange_purchase_auto_complete()
        if self._context.get('perfect_purchase_vendor_bill_id'):
            self.purchase_vendor_bill_id = self._context.get(
                'perfect_purchase_vendor_bill_id'
            )

    @api.depends('branch_id')
    def _onchange_branch_id(self):
        if self.branch_id:
            for line in self.line_ids:
                line.branch_id = self.branch_id
