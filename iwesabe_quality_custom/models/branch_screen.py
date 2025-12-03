# -*- coding: utf-8 -*-

from odoo import models, fields


class BranchScreen(models.Model):
    _name = "branch.screen"
    _description = "Branch Screen"

    name = fields.Char()
    franchise_id = fields.Many2one('franchise.screen', string="franchise")
