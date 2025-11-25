# * coding: utf8 *
###########################################################

from odoo import api, models, fields, _
from odoo.tools.safe_eval import safe_eval


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    branch_id = fields.Many2one(
        'res.branch', 'Branch', 
        related='move_id.branch_id',
        readonly=True,
        store=True
    )

    @api.onchange('account_id')
    def _inverse_account_id(self):
        super(AccountMoveLine, self)._inverse_account_id()
        if self.move_id.branch_id:
            self.branch_id = self.move_id.branch_id
