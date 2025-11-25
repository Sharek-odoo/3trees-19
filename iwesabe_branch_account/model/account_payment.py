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
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def default_get(self, fields):
        items = []
        rec = super(AccountPayment, self).default_get(fields)
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        if active_model or active_ids:
            invoices = self.env[active_model].browse(active_ids)
            if hasattr(invoices[0], 'branch_id'):
                rec['branch_id'] = invoices[0].branch_id.id
        return rec

    branch_id = fields.Many2one(
        'res.branch', string='Branch'
    )
    destination_branch_id = fields.Many2one(
        'res.branch', string='Destination Branch'
    )

    def _get_counterpart_move_line_vals(self, invoice=False):

        res = super(AccountPayment, self)._get_counterpart_move_line_vals(
            invoice=invoice
        )
        res.update({
            'branch_id': self.branch_id.id,
        })
        return res

    def _get_liquidity_move_line_vals(self, amount):
        res = super(AccountPayment, self)._get_liquidity_move_line_vals(amount)
        res.update({'branch_id': self.branch_id.id})
        return res

    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconciliable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_(
                    "The payment cannot be processed because the invoice is not open!"
                ))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(
                    ir_sequence_date=rec.payment_date
                ).next_by_code(
                    sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_(
                        "You have to define a sequence for %s in your company."
                    ) % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') \
                and 1 or -1)
            move = rec._create_payment_entry(amount)
            if move:
                move.branch_id = rec.branch_id.id
            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(
                    lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()

            rec.write({'state': 'posted', 'move_name': move.name})
        return True

    def _create_payment_entry(self, amount):
        res = super(AccountPayment, self)._create_payment_entry(amount)
        if not self.branch_id:
            return res
        move_id = res
        move_id.branch_id = self.branch_id.id
        for line in move_id.line_ids:
            line.branch_id = self.branch_id.id

        return res

    def _create_transfer_entry(self, amount):
        res = super(AccountPayment, self)._create_transfer_entry(amount)

        if self.payment_type != 'transfer':
            return res
        move_id = res.move_id
        move_id.branch_id = self.destination_branch_id.id

        for line in move_id.line_ids:
            line.branch_id = self.destination_branch_id.id
        return res
