# * coding: utf8 *
##############################################################################
#
#    Global Creative Concepts Tech Co Ltd.
#    Copyright (C) 2018TODAY iWesabe (<http://www.iwesabe.com>).
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from odoo.osv.expression import AND
from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class SaleReport(models.Model):
    _inherit = "sale.report"

    branch_id = fields.Many2one('res.branch')

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['branch_id'] = "s.branch_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            s.branch_id"""
        return res

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        user_branch_ids = self.env.user.branch_ids.ids
        _logger.info(
            "Read Group Data:\n\n\n'Domain: %s \n Type of Domain: %s'\n\n\n"
            % (domain, type(domain))
        )
        domain = AND([domain, [('branch_id', 'in', user_branch_ids)]])

        res = super(SaleReport, self).read_group(
            domain,
            fields,
            groupby,
            offset=0,
            limit=None,
            orderby=False,
            lazy=True
        )

        return res
