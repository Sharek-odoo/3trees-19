from odoo import models, fields, api

# class MrpBom(models.Model):
#     _inherit = 'mrp.bom'

    # @api.onchange('product_qty')
    # def _onchange_product_qty_update_net_quantity(self):
    #     """Update net_quantity and recalculate product_qty for all BOM lines based on BOM's product_qty."""
    #     for line in self.bom_line_ids:
    #         # Update net_quantity
    #         line.net_quantity = self.product_qty
    #
    #         # Recalculate product_qty based on loss_percentage
    #         if line.loss_percentage < 100:  # Prevent division by zero or invalid percentages
    #             line.product_qty = line.net_quantity / (1 - (line.loss_percentage / 100))
    #         else:
    #             line.product_qty = 0  # Default to 0 if Loss % is invalid


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    net_quantity = fields.Float(string="Net Qty", help="Enter the net quantity for this line.")
    loss_percentage = fields.Float(string="Loss %", help="Enter the loss percentage for this line.")

    @api.onchange('net_quantity', 'loss_percentage')
    def _onchange_calculate_product_qty(self):
        """Auto-update product_qty based on Net Qty and Loss %."""
        for line in self:
            if line.loss_percentage < 100:  # Prevent division by zero or invalid percentages
                line.product_qty = line.net_quantity / (1 - (line.loss_percentage / 100))
            else:
                line.product_qty = 0  # Default to 0 if Loss % is invalid
