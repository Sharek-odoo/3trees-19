	#  -*-coding- utf8-*-

from odoo import fields , models 

class SaleOrder(models.Model):
	_inherit = "stock.warehouse"

	user_ids = fields.Many2many("res.users",string="User's")