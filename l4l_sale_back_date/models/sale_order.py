# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_confirmation_values(self):
        rec = super()._prepare_confirmation_values()
        if self.company_id.l4l_allow_back_date:
            rec.update({
                'date_order': self.date_order
            })
        return rec

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
