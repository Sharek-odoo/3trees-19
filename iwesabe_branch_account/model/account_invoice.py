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


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    branch_id = fields.Many2one('res.branch', 'Branch')

    @api.onchange('branch_id')
    def onchange_branch_id(self):
        if self.branch_id:
            if self.branch_id.term_conditions1:
                self.comment = self.branch_id.term_conditions1

    def action_move_create(self):
        result = super(AccountInvoice, self).action_move_create()
        for inv in self:
            inv.move_id.branch_id = self.branch_id.id
            for move_line in inv.move_id.line_ids:
                move_line.branch_id = self.branch_id.id
        return result

    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()
        # to write branch of account invoice in account invoice line
        for inv in self:
            if inv.branch_id:
                for line in inv.invoice_line_ids:
                    line.branch_id = inv.branch_id.id
        return res
