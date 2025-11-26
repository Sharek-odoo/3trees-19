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


from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class StockQuant(models.Model):
	_inherit = 'stock.quant'

	branch_id = fields.Many2one(
		related='location_id.branch_id',
		string='Branch',
		store=True,
		readonly=True
	)

	@api.onchange('branch_id', 'warehouse_id')
	def update_branch_data(self):
		self.update({
			'branch_id': self.warehouse_id.branch_id.id
		})

	def _get_inventory_move_values(self, qty, location_id, location_dest_id, out=False):
		res = super()._get_inventory_move_values(qty,location_id,location_dest_id,out)
		res.update({'branch_id':self.branch_id.id})
		return res