from odoo import models, fields, api, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    short_code = fields.Char(string='Short Code')
