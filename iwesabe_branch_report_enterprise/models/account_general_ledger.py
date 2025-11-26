# * coding: utf8 *


from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from datetime import timedelta
from odoo.tools import float_is_zero


class report_account_general_ledger(models.AbstractModel):
	_inherit = "account.general.ledger.report.handler"


	def _get_aml_values(self, report, options, expanded_account_ids, offset=0, limit=None):
		return super()._get_aml_values(report, options, expanded_account_ids, offset,limit)

