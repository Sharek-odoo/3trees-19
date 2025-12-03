# -*- coding: utf-8 -*-

from odoo import models, fields


class FranchiseScreen(models.Model):
    _name = "franchise.screen"
    _description = "Franchise Screen"

    name = fields.Char()
    