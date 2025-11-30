from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    vehicle = fields.Char(string='Vehicle')
    city = fields.Char(string='City')
    driver_id = fields.Many2one('res.partner', 'Driver', tracking=True, help='Driver address of the vehicle', copy=False)
    mobile = fields.Char(string='Mobile')
