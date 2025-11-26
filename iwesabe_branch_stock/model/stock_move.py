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


class StockMove(models.Model):
	_inherit = 'stock.move'

	@api.model
	def _get_default_branch(self):
		User = self.env['res.users']
		return User.browse(self.env.uid).branch_id.id or False

	branch_id = fields.Many2one(
		'res.branch', 
		'Branch', 
		default=_get_default_branch
	)

	def _get_new_picking_values(self):
		res = super(StockMove, self)._get_new_picking_values()
		if self.branch_id:
			res.update({
				'branch_id': self.branch_id.id
			})
		else:
			stock =res['location_id']
			if stock:
				location = self.env['stock.location'].browse(stock)
				if location.branch_id:
					res.update({
						'branch_id': location.branch_id.id
					})
		return res

	def _prepare_account_move_vals(self, credit_account_id, 
		debit_account_id, journal_id, qty, description, svl_id, cost):
		self.ensure_one()
		move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, svl_id, description)
		date = self._context.get(
			'force_period_date', 
			fields.Date.context_today(self)
		)
		
		branch_id = self.branch_id
		if self.picking_id:
			branch_id = self.picking_id.branch_id

		return {
			'journal_id': journal_id,
			'line_ids': move_lines,
			'date': date,
			'ref': description,
			'stock_move_id': self.id,
			'stock_valuation_layer_ids': [(6, None, [svl_id])],
			'move_type': 'entry',
			'branch_id': branch_id.id,

		}

	def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, svl_id, description):
		self.ensure_one()
		rslt = super(StockMove, self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, svl_id, description)
		branch_id = self.branch_id
		if self.picking_id:
			branch_id = self.picking_id.branch_id
		rslt['credit_line_vals']['branch_id'] = branch_id.id
		rslt['debit_line_vals']['branch_id'] = branch_id.id
		return rslt