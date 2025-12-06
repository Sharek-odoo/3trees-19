from odoo import api, fields, models

class AccountBalanceSheetReportHandler(models.AbstractModel):
    _inherit = 'account.balance.sheet.report.handler'

    filter_branch = True