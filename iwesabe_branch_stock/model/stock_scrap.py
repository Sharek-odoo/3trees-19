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

from odoo import models, api, fields


class StockWarehouse(models.Model):
    _inherit = 'stock.scrap'

    branch_id = fields.Many2one('res.branch')

    @api.onchange('branch_id', 'picking_id')
    def update_branch_data(self):
        self.update({
            'branch_id': self.picking_id.branch_id.id
        })

    def _prepare_move_values(self):
        self.ensure_one()
        res = super(StockWarehouse, self)._prepare_move_values()
        res.update({
            'branch_id': self.branch_id and self.branch_id.id or False
        })
        return res
