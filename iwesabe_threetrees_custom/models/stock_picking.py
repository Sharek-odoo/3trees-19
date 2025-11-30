from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    vehicle = fields.Many2one('fleet.vehicle',string='Vehicle')
    city = fields.Char(string='City')
    driver_id = fields.Many2one('res.partner', 'Driver', tracking=True, help='Driver address of the vehicle', copy=False)
    mobile = fields.Char(string='Mobile')
