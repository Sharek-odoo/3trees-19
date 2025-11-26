# * coding: utf8 *


from odoo import models, fields, api, _
from odoo.tools import float_is_zero
from datetime import timedelta


class AccountPartnerLedger(models.AbstractModel):
    _inherit = 'account.partner.ledger.report.handler'

    # def _custom_options_initializer(self, report, options, previous_options=None):
    #     super()._custom_options_initializer(report, options, previous_options=previous_options)
    #     domain = []
    #
    #     if options.get('branch') and options.get('branch_ids'):
    #         branch_ids = [int(branch) for branch in options['branch_ids']]
    #         domain += (('branch_id', 'in', branch_ids))
    #
    #     options['forced_domain'] = options.get('forced_domain', []) + domain
