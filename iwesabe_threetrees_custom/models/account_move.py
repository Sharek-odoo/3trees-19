from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_arabic_name = fields.Char(string='Customer Arabic Name')
