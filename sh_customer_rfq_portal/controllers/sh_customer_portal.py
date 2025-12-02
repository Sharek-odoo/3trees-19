# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, fields
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import json


class CustomerRfqProductPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'customer_portal_rfq_count' in counters:
            customer_portal_rfq_count = request.env['purchase.order'].search_count()
            values['customer_portal_rfq_count'] = customer_portal_rfq_count
        return values
        # values.update({'customer_portal_rfq_count': '0'})        
        # return values

    def _prepare_portal_layout_values(self):
        values = super(CustomerRfqProductPortal,
                       self)._prepare_portal_layout_values()
        values.update({
            'page_name': 'customer_rfq_portal',
            'default_url': '/my/customer_portal_rfq',
        })
        return values

    @http.route(['/my/customer_portal_rfq'], type='http', auth="user", website=True)
    def portal_my_requestproduct_customer_rfq(self, **kw):
        values = self._prepare_portal_layout_values()
        return request.render("sh_customer_rfq_portal.sh_portal_request_customer_rfq_product", values)

    @http.route(['/my/customer_rfq_create'], type='http', auth="user", website=True)
    def create_customer_rfq(self, **post):
        if not post:
            return request.redirect('/my/customer_portal_rfq')
        
        # Check if at least the first product exists
        if not post.get('product_id_1'):
            return request.redirect('/my/customer_portal_rfq')

        # Remove hidden field if exists
        post.pop('js_id_product_list', None)

        counter = 0
        lines = []
        quote_msg = {}

        # Iterate over posted product rows
        while True:
            counter += 1
            product_key = f'product_id_{counter}'
            qty_key = f'total_qty_{counter}'

            if product_key not in post:
                break

            product_id = post.get(product_key)
            total_qty = post.get(qty_key)

            if not product_id:
                continue

            product = request.env['product.product'].sudo().search([('id', '=', int(product_id))], limit=1)
            if not product:
                continue

            line_vals = {
                'product_id': product.id,
                'name': product.name,
                'product_uom_id': product.uom_id.id,
                'product_uom_qty': float(total_qty) if total_qty not in ['', None, '0'] else 1.0
            }
            lines.append((0, 0, line_vals))

        # Create sale order
        if lines:
            order_id = request.env['sale.order'].sudo().create({
                'partner_id': request.env.user.partner_id.id,
                'date_order': fields.Datetime.now(),
                'company_id': request.env.company.id,
                'partner_invoice_id': int(post.get('js_id_invoice_address_list')),
                'partner_shipping_id': int(post.get('js_id_shipping_address_list')),
            })

            order_id.user_id = order_id.partner_id.user_id or order_id.partner_id.commercial_partner_id.user_id or request.env.user

            if post.get('note'):
                order_id.sudo().write({'note': post.get('note')})
            order_id.order_line = lines

            quote_msg = {'success': f'Quotation {order_id.name} created successfully.'}

        values = {
            'page_name': 'customer_rfq_portal',
            'default_url': '/my/customer_portal_rfq',
            'quote_msg': quote_msg,
        }
        return request.render("sh_customer_rfq_portal.sh_portal_request_customer_rfq_product", values)

    @http.route('/pack-qty-data', type="http", auth="public", website=True, csrf=False)
    def pack_qty_data(self, **kw):
        dic = {}
        if kw.get('product_id') and kw.get('product_id') != '':
            product_id = request.env['product.product'].sudo().search(
                [('id', '=', int(kw.get('product_id')))], limit=1)
            if product_id and product_id.image_1920:
                dic.update({
                    'image': '/web/image/product.product/'+str(product_id.id)+'/image_256',
                })
        return json.dumps(dic)
