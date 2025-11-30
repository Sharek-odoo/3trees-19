from odoo import fields, models, api


class FleetVehicleOdometer(models.Model):
    _inherit = 'fleet.vehicle.odometer'

    city = fields.Char(string='City')
    mobile = fields.Char(string='Mobile')

    @api.onchange('driver_id')
    def onchange_driver_mobile(self):
        for rec in self:
            if rec.driver_id:
                rec.mobile = rec.driver_id.mobile