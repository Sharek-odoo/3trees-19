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
import time
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round, float_repr, float_is_zero

class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.model
    def default_get(self, fields):
        res = super(AccountBankStatement, self).default_get(fields)
        res['branch_id'] = self.env['res.users'].browse(self.env.uid).branch_id.id
        return res

    @api.depends('previous_statement_id', 'previous_statement_id.balance_end_real')
    def _compute_ending_balance(self):
        latest_statement = self.env['account.bank.statement'].search([
            ('journal_id', '=', self[0].journal_id.id), 
            ('branch_id', '=', self[0].branch_id.id)],
            limit=1
        )
        for statement in self:
            # recompute balance_end_real in case we are in a bank journal and if we change the
            # balance_end_real of previous statement as we don't want
            # holes in case we add a statement in between 2 others statements.
            # We only do this for the bank journal as we use the balance_end_real in cash
            # journal for verification and creating cash difference entries so we don't want
            # to recompute the value in that case
            if statement.journal_type == 'bank':
                # If we are on last statement and that statement already has a balance_end_real, don't change the balance_end_real
                # Otherwise, recompute balance_end_real to prevent holes between statement.
                if latest_statement.id and statement.id == latest_statement.id \
                    and not float_is_zero(
                        statement.balance_end_real, 
                        precision_digits=statement.currency_id.decimal_places
                ):
                    statement.balance_end_real = statement.balance_end_real or 0.0
                else:
                    total_entry_encoding = sum([
                        line.amount for line in statement.line_ids
                    ])
                    statement.balance_end_real = statement.previous_statement_id\
                        .balance_end_real + total_entry_encoding
            else:
                # Need default value
                statement.balance_end_real = statement.balance_end_real or 0.0

    @api.depends('date', 'journal_id')
    def _get_previous_statement(self):
        for st in self:
            # Search for the previous statement
            domain = [
                ('date', '<=', st.date), 
                ('journal_id', '=', st.journal_id.id),
                ('branch_id', '=', st.branch_id.id)
            ]
            # The reason why we have to perform this test is because we have two use case here:
            # First one is in case we are creating a new record, in that case that new record does
            # not have any id yet. However if we are updating an existing record, the domain date <= st.date
            # will find the record itself, so we have to add a condition in the search to ignore self.id
            if not isinstance(st.id, models.NewId):
                domain.extend([
                    '|', '&', 
                    ('id', '<', st.id), 
                    ('date', '=', st.date), 
                    '&', ('id', '!=', st.id),
                    ('date', '!=', st.date)
                ])
            previous_statement = self.search(domain, limit=1)
            st.previous_statement_id = previous_statement.id

    branch_id = fields.Many2one('res.branch', required=False)
