from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_arabic_name = fields.Char(string='Product Arabic Name')

    @api.model_create_multi
    def create(self, vals_list):
        """ generate internal refenrence based on product category short code """
        for vals in vals_list:
            if 'categ_id' in vals:
                prefix = self.env['ir.sequence'].next_by_code('product.internal.refenrence') or _('New')
                category = self.env['product.category'].browse(vals.get('categ_id'))
                if category.short_code:
                    vals['default_code'] = '%s %s' % (category.short_code, prefix)
        return super(ProductTemplate, self).create(vals)
