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

import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        user_branch = self.env['res.users'].browse(self.env.uid).branch_id
        if user_branch:
            branched_warehouse = self.env['stock.warehouse'].search([
                ('branch_id', '=', user_branch.id)
            ])
            if branched_warehouse:
                res['warehouse_id'] = branched_warehouse.ids[0]
            else:
                res['warehouse_id'] = False

        return res

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['branch_id'] = self.branch_id.id
        return res

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            user_branch = self.env['res.users'].browse(self.env.uid).branch_id
            branched_warehouse = self.env['stock.warehouse'].search([
                ('branch_id', '=', user_branch.id)
            ], limit=1)
            if user_branch and branched_warehouse:
                self.warehouse_id = branched_warehouse.id
            else:
                warehouse_id = self.env['ir.default']._get_model_defaults(
                    'sale.order'
                ).get('warehouse_id')
                self.warehouse_id = warehouse_id or self.user_id.with_company(
                    self.company_id.id)._get_default_warehouse_id().id

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        if self.branch_id:
            branched_warehouse = self.env['stock.warehouse'].search([
                ('branch_id', '=', self.branch_id.id)
            ], limit=1)
            if branched_warehouse:
                self.warehouse_id = branched_warehouse.id
            else:
                self.warehouse_id = False

    @api.onchange('warehouse_id')
    def _onchange_warehouse_id(self):
        self.branch_id = False
        if self.warehouse_id and self.warehouse_id.branch_id:
            self.branch_id = self.warehouse_id.branch_id.id

    @api.onchange('partner_id')
    def update_warehouse(self):
        if self.partner_id:
            branched_warehouse = self.env['stock.warehouse'].search([
                ('branch_id', '=', self.branch_id.id)
            ], limit=1)
            if branched_warehouse:
                self.warehouse_id = branched_warehouse.id
            else:
                self.warehouse_id = False
