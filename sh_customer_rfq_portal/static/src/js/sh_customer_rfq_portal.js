/** @odoo-module **/
import PublicWidget from "@web/legacy/js/public/public_widget";

PublicWidget.registry.ShCustomerRfqPortal = PublicWidget.Widget.extend({
    selector: '.js_cls_customer_rdq_create_form',

    events: {
        'click #addBtn': '_onClickAddButton',
        'click .remove': '_onClickRemoveRow',
        'change .js_product_id': '_onChangeProductId',
    },

    /**
     * Mounted lifecycle hook
     */
    mounted() {
        // Prevent form resubmission on refresh
        if (window.history.replaceState) {
            window.history.replaceState(null, null, window.location.href);
        }
    },

    /**
     * Add a new product row
     */
    _onClickAddButton() {
        const tbody = document.querySelector("#tbody");
        if (!tbody) return;

        const rowCount = tbody.querySelectorAll("tr").length + 1;
        const productSelectName = `product_id_${rowCount}`;
        const totalQtyName = `total_qty_${rowCount}`;
        const productOptions = document.querySelector("#js_id_product_list")?.innerHTML || '';

        const rowHtml = `
            <tr id="R${rowCount}">
                <td class="text-center">
                    <img class="img img-fluid js_product_img"
                         src="/web/static/img/placeholder.png"
                         style="width:100px;height:100px;">
                </td>
                <td class="row-index text-center">
                    <select class="form-control form-field o_website_form_required_custom js_product_id"
                            name="${productSelectName}" required="True">
                        ${productOptions}
                    </select>
                </td>
                <td class="text-center">
                    <input class="form-control js_total_pack_qty"
                           type="number" value="1" name="${totalQtyName}">
                </td>
                <td class="text-center">
                    <button class="btn btn-danger remove" type="button">
                        <i class="fa fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;

        tbody.insertAdjacentHTML('beforeend', rowHtml);
    },

    /**
     * Remove a product row
     */
    _onClickRemoveRow(ev) {
        const row = ev.currentTarget.closest("tr");
        if (row) row.remove();
    },

    /**
     * Update product image on selection
     */
    _onChangeProductId(ev) {
        const $product = $(ev.currentTarget);
        const product_id = $product.val();
        const $img = $product.closest("tr").find(".js_product_img");

        // Reset to placeholder
        $img.attr("src", "/web/static/img/placeholder.png");

        if (!product_id) return;

        // Ajax call to get product image
        $.ajax({
            url: "/pack-qty-data",
            type: "POST",
            data: { product_id },
            success: function (result) {
                try {
                    const data = JSON.parse(result);
                    if (data.image) {
                        $img.attr("src", data.image);
                    }
                } catch (err) {
                    console.error("Invalid JSON from /pack-qty-data", err);
                }
            },
            error: function () {
                console.error("Failed to fetch product image.");
            }
        });
    },
});
