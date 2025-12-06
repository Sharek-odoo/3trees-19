# * coding: utf8 *


from odoo import models, fields, api, _


class AccountReport(models.Model):
    _inherit = 'account.report'

    filter_branch = fields.Boolean(
        string="Branch",
        compute=lambda x: x._compute_report_option_filter('filter_branch', True), readonly=False, store=True,
        depends=['root_report_id', 'section_main_report_ids'],
        precompute=True,
    )

    @api.model
    def _init_options_branch(self, options, previous_options=None):

        if not self.filter_branch:
            return

        options['branch'] = True
        res_branch_obj = self.env['res.branch']
        options['branch_ids'] = previous_options and previous_options.get('branch_ids') or []
        print('+++++++++++++++++++++++++++++++++++++++++++++', res_branch_obj)
        selected_branch_ids = [int(branch) for branch in options['branch_ids']]
        selected_branches = selected_branch_ids and res_branch_obj.browse(
            selected_branch_ids) or res_branch_obj
        options['selected_branch_ids'] = selected_branches.mapped('name')


    def _set_context(self, options):
        ctx = super(AccountReport, self)._set_context(options)
        if options.get('branch_ids'):
            ctx['branch_ids'] = self.env['res.branch'].browse(
                [int(branch) for branch in options['branch_ids']]).ids
        return ctx

    def get_report_informations(self, previous_options):
        if not previous_options:
            previous_options = {}
        options = self._get_options(previous_options)
        if options.get('branch'):
            options['selected_branch_ids'] = [self.env['res.branch'].browse(
                int(branch)).name for branch in options['branch_ids']]
        return super(AccountReport, self).get_report_informations(options)

    @api.model
    def _get_options_domain(self, options, date_scope):
        domain = super(AccountReport, self)._get_options_domain(options, date_scope)
        if options.get('branch') and options.get('branch_ids'):
            branch_ids = [int(branch) for branch in options['branch_ids']]
            domain.append(('branch_id', 'in', branch_ids))
        return domain
