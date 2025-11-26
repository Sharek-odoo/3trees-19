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
from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    branch_id = fields.Many2one('res.branch')

    def _select(self):
        return super(PurchaseReport, self)._select() + ", po.branch_id as branch_id"

    def _group_by(self):
        return super(PurchaseReport, self)._group_by() + ", po.branch_id"

    # @property
    # def _table_query(self):
    #     user_branch_ids = self.env.user.branch_ids.ids
    #     '''
    #         Report needs to be dynamic to take into account
    #         multi-company selected + multi-currency rates
    #     '''
    #     where_clause = '''
    #         WHERE po.branch_id in %s
    #     ''' % user_branch_ids
    #     qry = '%s %s %s %s' % (self._select(), self._from(),
    #                            self._group_by(), where_clause)
    #     _logger.info("Purchase Report Table Query\n\n'%s'\n\n" % qry)
    #     return qry

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        user_branch_ids = self.env.user.branch_ids.ids
        # if domain:
        #     domain.insert(3, "&")
        #     domain.insert(len(domain), ['branch_id', 'in', user_branch_ids])
        # else:
        domain = [['branch_id', 'in', user_branch_ids]]

        _logger.info(
            "Read Group Data:\n\n\n'Domain: %s \n Type of Domain: %s'\n\n\n"
            % (domain, type(domain))
        )
        res = super(PurchaseReport, self).read_group(
            domain,
            fields,
            groupby,
            offset=0,
            limit=None,
            orderby=False,
            lazy=True
        )

        return res
