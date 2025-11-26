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

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    branch_id = fields.Many2one('res.branch', 'Branch')

    def _create_workorder(self):
        for production in self:
            if not production.bom_id:
                continue
            workorders_values = []

            product_qty = production.product_uom_id._compute_quantity(
                production.product_qty, 
                production.bom_id.product_uom_id
            )
            exploded_boms, dummy = production.bom_id.explode(
                production.product_id,
                product_qty / production.bom_id.product_qty, 
                picking_type=production.bom_id.picking_type_id
            )

            for bom, bom_data in exploded_boms:
                # If the operations of the parent BoM and phantom BoM are the same, don't recreate work orders.
                if not (bom.operation_ids and (
                    not bom_data['parent_line'] or bom_data[
                        'parent_line'
                    ].bom_id.operation_ids != bom.operation_ids)
                ):
                    continue
                for operation in bom.operation_ids:
                    workorders_values += [{
                        'name': operation.name,
                        'production_id': production.id,
                        'workcenter_id': operation.workcenter_id.id,
                        'product_uom_id': production.product_uom_id.id,
                        'operation_id': operation.id,
                        'state': 'pending',
                        'consumption': production.consumption,
                        'branch_id': production.branch_id \
                            and production.branch_id.id or False
                    }]
            production.workorder_ids = [(5, 0)] + [(0, 0, value) \
                for value in workorders_values]
            for workorder in production.workorder_ids:
                workorder.duration_expected = workorder._get_duration_expected()

    def _get_move_finished_values(self, product_id, product_uom_qty, 
        product_uom, operation_id=False, byproduct_id=False):
        res = super(MrpProduction, self)._get_move_finished_values(
            product_id, product_uom_qty, product_uom, 
            operation_id=False, byproduct_id=False)
        res.update({
            'branch_id': self.branch_id and self.branch_id.id or False,
        })
        return res

    def _get_move_raw_values(self, product_id, product_uom_qty, 
        product_uom, operation_id=False, bom_line=False):
        res = super(MrpProduction, self)._get_move_raw_values(product_id, 
            product_uom_qty, product_uom, operation_id=False, bom_line=False)
        res.update({
            'branch_id': self.branch_id and self.branch_id.id or False,
        })
        return res

    def _post_inventory(self, cancel_backorder=False):
        for order in self:
            moves_not_to_do = order.move_raw_ids.filtered(lambda x: x.state == 'done')
            moves_to_do = order.move_raw_ids.filtered(
                lambda x: x.state not in ('done', 'cancel')
            )
            finish_moves = order.move_finished_ids.filtered(
                lambda m: m.product_id == order.product_id \
                    and m.state not in ('done', 'cancel'))
            for move in finish_moves:
                move.branch_id = order.branch_id
            for move in moves_to_do:
                move.branch_id = order.branch_id
            for move in moves_not_to_do:
                move.branch_id = order.branch_id
        return super(MrpProduction, self)._post_inventory(cancel_backorder)

    @api.model_create_multi
    def create(self, vals_list):
        production = super(MrpProduction, self).create(vals_list)
        for vals in vals_list:
            if vals.get('location_src_id', False):
                location_id = self.env['stock.location'].browse(
                    vals.get('location_src_id')
                )
                if location_id.branch_id:
                    production.branch_id = location_id.branch_id
        return production

    @api.onchange('picking_type_id')
    def onchange_picking_type_id(self):
        if self.picking_type_id:
            self.branch_id = self.picking_type_id.warehouse_id.branch_id.id

    @api.onchange('branch_id')
    def onchange_branch_id(self):
        if self.branch_id:
            warehouse = self.env['stock.warehouse'].search([
                ('company_id', '=', self.env.company.id),
                ('branch_id', '=', self.branch_id.id)
            ], limit=1)

            if warehouse:
                picking_type = warehouse.manu_type_id

                self.picking_type_id = picking_type.id

                self.location_src_id = (
                    picking_type.default_location_src_id.id
                    if picking_type.default_location_src_id
                    else warehouse.lot_stock_id.id
                )

                self.location_dest_id = (
                    picking_type.default_location_dest_id.id
                    if picking_type.default_location_dest_id
                    else warehouse.lot_stock_id.id
                )
            else:
                self.picking_type_id = False
                self.location_src_id = False
                self.location_dest_id = False


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    branch_id = fields.Many2one('res.branch', 'Branch')
