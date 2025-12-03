from odoo import models, fields, api, Command, _
import logging

_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    # @api.onchange('product_qty')
    # def _onchange_product_qty_update_net_quantity(self):
    #     """Update net_quantity and recalculate product_qty for all BOM lines based on BOM's product_qty."""
    #     for line in self.move_raw_ids:
    #         # Update net_quantity
    #         line.net_quantity = self.product_qty
    #
    #         # Recalculate product_qty based on loss_percentage
    #         if line.loss_percentage < 100:  # Prevent division by zero or invalid percentages
    #             line.product_uom_qty = line.net_quantity / (1 - (line.loss_percentage / 100))
    #         else:
    #             line.product_uom_qty = 0  # Default to 0 if Loss % is invalid

    @api.onchange('product_qty')
    def _onchange_product_qty_update_net_quantity(self):
        """Update net_quantity and recalculate product_qty for all BOM lines based on BOM's product_qty."""
        for line in self.move_raw_ids:
            # Get the planned BOM quantity and MO quantity
            planned_bom_qty = self.bom_id.product_qty  # BOM Product Qty
            planned_to_consume = line.bom_line_id.net_quantity  # BOM Line Product Qty (To Consume)


            line.net_quantity = planned_to_consume * (self.product_qty / planned_bom_qty)

            # Recalculate product_uom_qty based on loss_percentage
            if line.loss_percentage < 100:  # Prevent division by zero or invalid percentages
                line.product_uom_qty = line.net_quantity / (1 - (line.loss_percentage / 100))
            else:
                line.product_uom_qty = 0  # Default to 0 if Loss % is invalid


    @api.depends('bom_id')
    def _compute_move_raw_ids(self):
        for production in self:
            if production.state != 'draft':
                continue

            # Store existing moves with their original values
            existing_moves = {
                move.bom_line_id.id: {
                    'move': move,
                    'product_uom_qty': move.bom_line_id.bom_id.product_qty,  # Store original BOM line quantity
                    'net_quantity': move.bom_line_id.net_quantity,
                    'loss_percentage': move.bom_line_id.loss_percentage
                } for move in production.move_raw_ids.filtered(lambda m: m.bom_line_id)
            }

            moves_raw_values = production._get_moves_raw_values()
            move_commands = []

            for move_raw_values in moves_raw_values:
                bom_line_id = move_raw_values.get('bom_line_id')
                if bom_line_id in existing_moves:
                    # Preserve original BOM line quantities
                    move_raw_values.update({
                        'product_uom_qty': existing_moves[bom_line_id]['product_uom_qty'],
                        'net_quantity': existing_moves[bom_line_id]['net_quantity'],
                        'loss_percentage': existing_moves[bom_line_id]['loss_percentage']
                    })
                    move_commands.append(Command.update(
                        existing_moves[bom_line_id]['move'].id,
                        move_raw_values
                    ))
                else:
                    move_commands.append(Command.create(move_raw_values))

            existing_move_ids = set(existing_moves.keys())
            bom_line_ids = {val['bom_line_id'] for val in moves_raw_values if 'bom_line_id' in val}
            to_delete = existing_move_ids - bom_line_ids

            for move_id in to_delete:
                move_commands.append(Command.delete(existing_moves[move_id]['move'].id))

            production.move_raw_ids = move_commands

    def _get_move_raw_values(self, product_id, product_uom_qty, product_uom, operation_id=False, bom_line=False):
        source_location = self.location_src_id

        # Use original BOM line net_quantity without multiplication
        initial_net_qty = bom_line.net_quantity if bom_line else product_uom_qty
        initial_loss_percentage = bom_line.loss_percentage if bom_line else 0.0

        # Initial calculation without multiplying by production quantity
        if initial_loss_percentage < 100:
            calculated_qty = initial_net_qty / (1 - (initial_loss_percentage / 100))
        else:
            calculated_qty = 0

        data = {
            'sequence': bom_line.sequence if bom_line else 10,
            'date': self.date_start,
            'date_deadline': self.date_start,
            'bom_line_id': bom_line.id if bom_line else False,
            'picking_type_id': self.picking_type_id.id,
            'product_id': product_id.id,
            'product_uom_qty': calculated_qty,
            'product_uom': product_uom.id,
            'location_id': source_location.id,
            'location_dest_id': self.product_id.with_company(self.company_id).property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            'operation_id': operation_id,
            'price_unit': product_id.standard_price,
            'procure_method': 'make_to_stock',
            'origin': self._get_origin(),
            'state': 'draft',
            'warehouse_id': source_location.warehouse_id.id,
            'reference_ids': self.reference_ids.ids,
            'propagate_cancel': self.propagate_cancel,
            'manual_consumption': self.env['stock.move']._determine_is_manual_consumption(bom_line),
            'net_quantity': initial_net_qty,
            'loss_percentage': initial_loss_percentage,
        }
        return data


class StockMove(models.Model):
    _inherit = 'stock.move'

    net_quantity = fields.Float(string="Net Qty", help="Enter the net quantity for this line.")
    loss_percentage = fields.Float(string="Loss %", help="Enter the loss percentage for this line.", store=True)

    product_uom_qty = fields.Float(
        string="To Consume",
        compute="_compute_to_consume",
        store=True,
        readonly=False
    )

    @api.depends('net_quantity', 'loss_percentage', 'raw_material_production_id.product_qty')
    def _compute_to_consume(self):
        """
        Auto-update product_uom_qty only when product_qty is explicitly changed.
        """
        for line in self:
            if line.loss_percentage < 100:  # Prevent division by zero or invalid percentages
                line.product_uom_qty = line.net_quantity / (1 - (line.loss_percentage / 100))
            else:
                line.product_uom_qty = 0  # Default to 0 if Loss % is invalid
