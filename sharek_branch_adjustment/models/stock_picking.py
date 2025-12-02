# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    

    adjustment = fields.Boolean(string='Adjustment')
    
    
    @api.onchange('adjustment','picking_type_id')
    def _onchange_adjustment(self):
        move_ids_without_package = [(5,0,0)]
        if self.adjustment and self.picking_type_id and self.picking_type_id.code == 'outgoing':
            products = self.location_id.quant_ids.filtered(lambda q: q.quantity != 0).mapped('product_id')
            if products:
                move_ids_without_package = [(0, 0, {
                    'name': product.name,
                    'product_id': product.id,
                    'product_uom_qty': 0.0,
                    'product_uom': product.uom_id.id,
                    'location_id': self.location_id.id,
                    'location_dest_id': self.location_dest_id.id,
                    'onhand_qty': product.with_context(location=self.location_id.id).qty_available,
                }) for product in products]
        self.move_ids_without_package = move_ids_without_package
        
    
    def action_picking_move_tree(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.stock_move_action")
        if self.adjustment:
            action['views'] = [
            (self.env.ref('sharek_branch_adjustment.view_picking_move_adjustment_tree').id, 'list'),
            ]
        else:
            action['views'] = [
                (self.env.ref('stock.view_picking_move_tree').id, 'list'),
            ]
        action['context'] = self.env.context
        action['domain'] = [('picking_id', 'in', self.ids)]
        return action

    def update_adjustment_moves(self):
        for picking in self:
            src_loc = picking.location_id
            for move in picking.move_ids_without_package:
                product = move.product_id
                # on hand في موقع المصدر
                onhand = product.with_context(location=src_loc.id).qty_available or 0.0
                # حوّل لوحدة قياس السطر
                if move.product_uom and move.product_uom != product.uom_id:
                    onhand = product.uom_id._compute_quantity(onhand, move.product_uom, rounding_method='HALF-UP')
                # خزّن قيمة on hand في حقل السطر قبل الـ onchange
                if 'onhand_qty' in move._fields:
                    move.onhand_qty = onhand
                elif 'onhand' in move._fields:
                    move.onhand = onhand
                # شغّل المنطق المعتمد على onhand
                move._onchange_count_qty()
    # def update_adjustment_moves(self):
    #     for record in self:
    #         for move in record.move_ids_without_package:
    #             move._onchange_count_qty()
    
class StockMove(models.Model):
    _inherit = 'stock.move'

    adjustment = fields.Boolean(string='Adjustment', related='picking_id.adjustment', store=True)
    onhand_qty = fields.Float(string='On Hand Quantity', digits='Product Unit of Measure',)
    count_qty = fields.Float(string='Counted Quantity', digits='Product Unit of Measure',)
    product_uom_qty = fields.Float(
        'Demand',
        digits='Product Unit of Measure',
        default=1.0, required=True, readonly=False, states={'done': [('readonly', True)]},
        compute='_compute_product_uom_qty',
        help="This is the quantity of products from an inventory "
             "point of view. For moves in the state 'done', this is the "
             "quantity of products that were actually moved. For other "
             "moves, this is the quantity of product that is planned to "
             "be moved. Lowering this quantity does not generate a "
             "backorder. Changing this quantity on assigned moves affects "
             "the product reservation, and should be done with care.")
    #
    # @api.depends('onhand_qty', 'count_qty', 'adjustment')
    # def _compute_product_uom_qty(self):
    #     for move in self:
    #         if move.adjustment and move.onhand_qty > 0:
    #             move.product_uom_qty = move.onhand_qty - move.count_qty
    #         else:
    #             move.product_uom_qty = move.onhand_qty + move.count_qty

    @api.depends('onhand_qty', 'count_qty', 'adjustment')
    def _compute_product_uom_qty(self):
        for move in self:
            if move.adjustment and move.onhand_qty > 0:
                move.product_uom_qty = move.onhand_qty - move.count_qty
            else:
                move.product_uom_qty = move.product_uom_qty or 1.0

    @api.onchange('count_qty', 'onhand_qty')
    def _onchange_count_qty(self):
        if self.onhand_qty > 0:
            self.product_uom_qty = self.onhand_qty - self.count_qty
    
