# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models,fields,api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    analytic_precision = fields.Integer(
        default=2,
        help="Precision for analytic distribution display"
    )

    analytic_distribution = fields.Json(
        string="Analytic Distribution",
        help="This analytic distribution will be copied to stock moves.",
    )

    @api.onchange('analytic_distribution')
    def _onchange_analytic_distribution(self):
        for picking in self:
            for move in picking.move_ids:
                move.analytic_distribution = picking.analytic_distribution
    def button_validate(self):
        self = self.with_context(validate_analytic=True)
        return super().button_validate()
