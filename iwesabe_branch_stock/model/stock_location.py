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

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class StockLocation(models.Model):
    _inherit = 'stock.location'

    branch_id = fields.Many2one('res.branch')

    @api.onchange('branch_id', 'warehouse_id')
    def update_branch_data(self):
        self.update({
            'branch_id': self.warehouse_id.branch_id.id
        })

    @api.constrains('branch_id')
    def _check_branch(self):
        warehouse_obj = self.env['stock.warehouse']
        warehouse_id = warehouse_obj.search(
            ['|', '|', ('wh_input_stock_loc_id', '=', self.id),
             ('lot_stock_id', '=', self.id),
             ('wh_output_stock_loc_id', '=', self.id)])
        for warehouse in warehouse_id:
            if self.branch_id != warehouse.branch_id:
                raise UserError(_(
                    'Configuration error\nYou  must select same branch on a location as assigned on a warehouse configuration.'
                ))
