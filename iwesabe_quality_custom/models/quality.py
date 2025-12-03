# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.tools.misc import formatLang


class QualityAlert(models.Model):
    _inherit = "quality.alert"


    franchise_id = fields.Many2one('franchise.screen', string="franchise")

    def action_send_notification(self):
        mail_template = self.env.ref('iwesabe_quality_custom.quality_alert_email_template')
        mail_template.send_mail(self.id, force_send=True)
        # channel = self.env['mail.channel'].search([('name', '=', 'general')], limit=1)
        self.message_post(
            body="<p> Yor product request has been checked </p>",
            auther_id=self.env.user.partner_id.id,
            message_type="notification",
            partner_ids=self.user_id.partner_id.ids)

        # admin_user_id = self.env.ref('base.user_root').id
        # msg = """
        #     <p> Yor product request has been checked </p>
        # """
        # if msg and channel:
        #     message_values = {
        #         'body': msg,
        #         'author_id': admin_user_id,
        #         'model': 'mail.channel',
        #         'res_id': channel.id,
        #         'message_type': 'comment',
        #     }
        #     self.env['mail.message'].create(message_values)quality.point



class QualityPoint(models.Model):
    _inherit = "quality.point"


    franchise_id = fields.Many2one('franchise.screen', string="franchise")


class QualityCheck(models.Model):
    _inherit = "quality.check"


    franchise_id = fields.Many2one('franchise.screen', string="franchise")
