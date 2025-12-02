from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    arabic_name = fields.Char(string='Arabic Name')