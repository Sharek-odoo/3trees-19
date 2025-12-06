# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

from odoo import api, models, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        res = super()._action_done()
        if self.company_id.l4l_allow_back_date:
            for picking in self:
                picking.date_done = picking.scheduled_date
                for move in picking.move_ids:
                    move.write({
                        'date': picking.scheduled_date,
                        'date_deadline': picking.scheduled_date,
                    })
                    move.move_line_ids.write({
                        'date': picking.scheduled_date,
                    })
                    val_layer_ids = self.env['product.value'].search([('move_id', '=', move.id)])
                    if val_layer_ids:
                        query = """update stock_valuation_layer set create_date ='""" + str(picking.scheduled_date) + """' where id in %s"""
                        params = (tuple(val_layer_ids.ids),)
                        self.env.cr.execute(query, params)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
