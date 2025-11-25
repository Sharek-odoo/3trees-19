# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from lxml import etree
from odoo.exceptions import UserError
import json
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount = fields.Float('Discount %')

    def _prepare_account_move_line(self, move=False):
        """
        Prepare account move line with discount and correct price_subtotal
        """
        result = super(PurchaseOrderLine, self)._prepare_account_move_line(move)

        if result:
            # Update price_subtotal with tax included
            result.update({
                'discount': self.discount,
            })
        return result

    @api.depends('price_unit', 'product_qty', 'discount', 'tax_ids')
    def _compute_amount(self):
        """
        Compute the price subtotal with discount and taxes applied.
        """
        for line in self:
            # Calculate subtotal before discount
            line_subtotal = line.price_unit * line.product_qty

            # Calculate discount amount
            line_discount = (line_subtotal * line.discount) / 100.0

            # Calculate discounted subtotal
            discounted_subtotal = line_subtotal - line_discount

            # Compute taxes on discounted price
            if line.tax_ids:
                taxes = line.tax_ids.compute_all(
                    line.price_unit * (1 - line.discount / 100.0),
                    quantity=line.product_qty,
                    currency=line.order_id.currency_id,
                    product=line.product_id,
                    partner=line.order_id.partner_id
                )
                tax_amount = sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                line.price_subtotal = discounted_subtotal
            else:
                line.price_subtotal = discounted_subtotal


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    operation_manager_id = fields.Many2one("res.users", domain=lambda self: [
        ("id", 'in', self.env.ref("purchase.group_purchase_manager").user_ids.ids)])
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_all')

    @api.depends('order_line.price_unit', 'order_line.product_qty', 'order_line.discount', 'order_line.tax_ids')
    def _amount_all(self):
        """
        Compute the total amounts: untaxed, tax, discount, and total.
        """
        for order in self:
            amount_untaxed = 0.0
            amount_tax = 0.0
            amount_discount = 0.0

            # Iterate through all lines to compute values
            for line in order.order_line.filtered(lambda l: not l.display_type):
                # Subtotal before discount
                line_subtotal = line.price_unit * line.product_qty
                # Discount amount for the line
                line_discount = (line_subtotal * line.discount) / 100.0
                # Compute discounted subtotal
                discounted_subtotal = line_subtotal - line_discount

                # Add to untaxed amount
                amount_untaxed += discounted_subtotal
                # Add to discount total
                amount_discount += line_discount

                # Compute taxes
                if line.tax_ids:
                    taxes = line.tax_ids.compute_all(
                        line.price_unit * (1 - line.discount / 100.0),  # Apply discount to price_unit
                        quantity=line.product_qty,
                        currency=order.currency_id,
                        product=line.product_id,
                        partner=order.partner_id
                    )
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))

            # Update all fields
            order.amount_untaxed = amount_untaxed
            order.amount_discount = amount_discount
            order.amount_tax = amount_tax
            order.amount_total = amount_untaxed + amount_tax

    def button_confirm(self):
        result = super().button_confirm()
        user_id = self.env['ir.config_parameter'].sudo().get_param('iwesabe_purchase_custom.user_id')
        user_id = self.env['res.users'].browse(int(user_id))
        if not user_id:
            raise UserError(_("Approval User is not configured in purchase settings!..."))
        else:
            if user_id.id != self.env.user.id or self.amount_total < self.env.company.po_double_validation_amount:
                raise UserError(_("You cannot confirm this purchase order!..."))
        return result

    def _prepare_account_move(self):
        """
        Override to include discount and other totals in the account move.
        """
        self.ensure_one()
        move_vals = super(PurchaseOrder, self)._prepare_account_move()

        # # Pass total amounts including the discount
        move_vals.update({
            'amount_untaxed': self.amount_untaxed,
            'amount_discount': self.amount_discount,
            'amount_tax': self.amount_tax,
            'amount_total': self.amount_total,
        })

        return move_vals


    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        """
        The function `get_view` modifies the XML view of a form by hiding a button if the current user is
        not the operation manager.
        Operation Managers: Are the users which are under the `group Project/Administrator`

        :param view_id: The view_id parameter is used to specify the ID of the view that you want to
        retrieve. If no view_id is provided, it will default to None
        :param view_type: The `view_type` parameter specifies the type of view to retrieve. In this case,
        it is set to `'form'`, indicating that the method is retrieving a form view, defaults to form
        (optional)
        :return: a dictionary named "result" which contains the modified view architecture.
        """
        result = super().get_view(view_id, view_type, **options)
        if view_type == 'form':
            doc = etree.XML(result['arch'])
            po = self.sudo().browse(self.env.context.get("params", {}).get("id"))
            if self.env.user.id != po.operation_manager_id.id:
                elem_to_hide_node = doc.xpath("//button[@name='button_approve']")
                for node in elem_to_hide_node:
                    node.set('invisible', '1')
                    node.set('class', 'd-none')
            result['arch'] = etree.tostring(doc, encoding='unicode')
        return result


# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'
#
#     @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', 'currency_id')
#     def _compute_totals(self):
#         """
#         Override to include taxes in price_subtotal.
#         """
#         for line in self:
#             if line.display_type != 'product':
#                 # Skip non-product lines
#                 line.price_total = line.price_subtotal = False
#                 continue
#
#             # Calculate discounted price per unit
#             line_discount_price_unit = line.price_unit * (1 - (line.discount / 100.0))
#
#             # Calculate subtotal before tax
#             subtotal = line.quantity * line_discount_price_unit
#
#             # Include taxes in price_subtotal
#             if line.tax_ids:
#                 taxes_res = line.tax_ids.compute_all(
#                     line_discount_price_unit,
#                     quantity=line.quantity,
#                     currency=line.currency_id,
#                     product=line.product_id,
#                     partner=line.partner_id,
#                     is_refund=line.is_refund,
#                 )
#                 # Add taxes to subtotal for price_subtotal
#                 line.price_subtotal = taxes_res['total_included']  # Include taxes in subtotal
#                 line.price_total = taxes_res['total_included']
#             else:
#                 # No taxes, use direct subtotal
#                 line.price_total = line.price_subtotal = subtotal

class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        """
        Override _action_done to adjust unit_cost in stock.valuation.layer
        """
        res = super(StockMove, self)._action_done(cancel_backorder)

        # Update stock valuation layer with discounted unit cost
        for move in self:
            if move.purchase_line_id:
                # Fetch purchase order line and calculate discounted unit cost
                discounted_unit_cost = move.purchase_line_id.price_unit * (1 - (move.purchase_line_id.discount / 100.0))

                # Find and update the stock valuation layer
                valuation_layers = self.env['stock.valuation.layer'].search([('stock_move_id', '=', move.id)])
                for valuation_layer in valuation_layers:
                    valuation_layer.unit_cost = discounted_unit_cost

        return res