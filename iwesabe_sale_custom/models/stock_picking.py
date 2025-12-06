from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if res is True:
            template_id = self.env.ref('iwesabe_sale_custom.mail_template_delivery_confirmation_customer')
            if self.sale_id and template_id:
                template_id.with_context().sudo().send_mail(self.id, force_send=True, email_values={
                    'email_to': self.sale_id.partner_id.email or ''})
            accountant_template_id = self.env.ref('iwesabe_sale_custom.mail_template_delivery_confirmation_accountant')
            account_manager_group_id = self.env.ref("account.group_account_manager").id
            account_users = self.env['res.users'].sudo().search([('groups_id', 'in', [account_manager_group_id])])
            if account_users and accountant_template_id:
                for rec in account_users:
                    accountant_template_id.with_context(user_name=rec.name).sudo().send_mail(self.id, force_send=True, email_values={'email_to': rec.email or rec.partner_id.email})
        return res
