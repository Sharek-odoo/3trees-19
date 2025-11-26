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

from odoo import models, api, fields, _
from odoo.exceptions import UserError
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrder, self).default_get(fields)
        user_branch = self.env['res.users'].browse(self.env.uid).branch_id
        if user_branch:
            branched_warehouse = self.env['stock.warehouse'].search([
                ('branch_id', '=', user_branch.id)]
            )
            if branched_warehouse:
                res['picking_type_id'] = branched_warehouse[0].in_type_id.id
            else:
                res['picking_type_id'] = False
        else:
            res['picking_type_id'] = False
        return res

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        res['branch_id'] = self.branch_id.id
        return res

    @api.onchange('picking_type_id')
    def _onchange_picking_type_id(self):
        if self.picking_type_id:
            self.branch_id = False
            self.branch_id = self.picking_type_id.warehouse_id \
                and self.picking_type_id.warehouse_id.branch_id.id \
                or self.branch_id.id

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        if self.branch_id:
            branched_warehouse = self.env['stock.warehouse'].search([
                ('branch_id', '=', self.branch_id.id)]
            )
            if branched_warehouse:
                self.picking_type_id = branched_warehouse[0].in_type_id.id
            else:
                self.picking_type_id = False

    # @api.model
    # def _default_picking_type(self):
    #     return self._get_picking_type(
    #         self.env.context.get('company_id')
    #         or self.env.company.id
    #     )

    # @api.model
    # def _get_picking_type(self, company_id):
    #     user_branch_ids = self.env.user.branch_ids
    #     picking_type = self.env['stock.picking.type'].search(
    #         [
    #             ('code', '=', 'incoming'),
    #             ('warehouse_id.company_id', '=', company_id),
    #             ('branch_id', 'in', user_branch_ids.ids)
    #         ])
    #     if not picking_type:
    #         picking_type = self.env['stock.picking.type'].search(
    #             [
    #                 ('code', '=', 'incoming'),
    #                 ('warehouse_id', '=', False),
    #                 ('branch_id', 'in', user_branch_ids.ids)
    #             ])
    #     return picking_type[:1]

    # @api.model
    # def _get_picking_type_domain(self):
    #     user_branch_ids = self.env.user.branch_ids
    #     return '''[
    #         ('branch_id', '=', %s),
    #         ('code', '=', 'incoming')
    #     ]''' % user_branch_ids.ids[0]

    # picking_type_id = fields.Many2one(
    #     'stock.picking.type',
    #     'Deliver To',
    #     states=Purchase.READONLY_STATES,
    #     required=True,
    #     default=_default_picking_type,
    #     domain="[('code', '=', 'incoming')]",
    #     help="This will determine operation type of incoming shipment"
    # )
