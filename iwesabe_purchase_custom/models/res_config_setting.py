#  -*-coding- utf8-*-

from odoo import fields , models 

class ResConfigSettings(models.TransientModel):
	_inherit = "res.config.settings"

	user_id = fields.Many2one("res.users",string="Purches Request Manger",
								config_parameter = "iwesabe_purchase_custom.user_id")
