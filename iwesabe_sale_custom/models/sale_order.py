from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    url = fields.Char('URL', compute='_compute_url')

    def _compute_url(self):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        action = self.env.ref("iwesabe_sale_custom.action_sale_picking_tree_all")
        record_url = False
        if self.picking_ids:
            record_url = base_url + "/web#view_type=list&model=stock.picking&active_id="+str(self.id)+"&action=" + str(action.id)
        self.url = record_url


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        # inventory_user_group_id = self.env.ref("stock.group_stock_user").id
        # inventory_manager_group_id = self.env.ref("stock.group_stock_manager").id
        # inventory_users = self.env['res.users'].sudo().search([('groups_id', 'in', [inventory_user_group_id]), ('groups_id', 'not in', [inventory_manager_group_id])])
        inventory_users = self.warehouse_id.user_ids
        template_id = self.env.ref('iwesabe_sale_custom.mail_template_sale_confirmation_inventory')
        if inventory_users and template_id:
            for rec in inventory_users:
                template_id.with_context(user_name=rec.name).sudo().send_mail(self.id, force_send=True, email_values={'email_to': rec.email or rec.partner_id.email})

                if self.url:
                    body = "<p>Hello " + rec.name + (",</p><p>This is to inform you that a new sale order has been confirmed and requires your attention in the inventory.</p>"
                                                     +" <p>Sale Order Details :</p>"
                                                     +"<ul><li>Order Reference: "+self.name+"</li>"+
                                                    "<li>Customer: "+self.name+"</li>"+
                                                    "<li>Total Amount: "+str(self.amount_total)+"</li>"
                                                    +"</ul>"+
                                                    "<a class='btn btn-primary' href='"+self.url+"' style='text-decoration:none;'>Delivery Note</a>"
                                                     +"<p>Please review and take necessary actions in the inventory system.</p><br/>"+
                                                     "<p>Thank you</p>"+
                                                     "<p>"+self.env.company.name+"</p>"
                                                     )
                else:
                    body = "<p>Hello " + rec.name + (
                                ",</p><p>This is to inform you that a new sale order has been confirmed and requires your attention in the inventory.</p>"
                                + " <p>Sale Order Details :</p>"
                                + "<ul><li>Order Reference: " + self.name + "</li>" +
                                "<li>Customer: " + self.name + "</li>" +
                                "<li>Total Amount: " + str(self.amount_total) + "</li>"
                                + "</ul>"
                                + "<p>Please review and take necessary actions in the inventory system.</p><br/>" +
                                " <p>Thank you</p>" +
                                "<p>" + self.env.company.name + "</p>"
                                )

                self.message_post(
                    body=body,
                    auther_id=self.env.user.partner_id.id,
                    message_type="notification",
                    partner_ids=rec.partner_id.ids)
        return res
