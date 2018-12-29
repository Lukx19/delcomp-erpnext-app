frappe.ui.form.on("Stock Entry", {
    onload_post_render: function (frm) {
        var grid = frm.get_field("items").grid
        grid.multiple_set = false
        var btn = $(grid.wrapper).find(".grid-add-multiple-rows");
        btn.off("click")
        // grid.set_multiple_add("item_code", "custom_quantity");
        grid.set_multiple_add("item_code");
    },

})

var update_uom_rate = function (cdt, cdn) {
    var row = locals[cdt][cdn]
    if (!row.item_code)
        return
    frappe.run_serially([
        () => frappe.timeout(2),
        () => frappe.call({
            method: "erpnext.stock.get_item_details.get_conversion_factor",
            args: {
                item_code: row.item_code,
                uom: "bm"
            },
            callback: function (r) {
                var conversion = r.message.conversion_factor
                if (conversion) {
                    frappe.model.set_value(cdt, cdn, "rate_in_uom", row.basic_rate * conversion)
                } else {
                    frappe.model.set_value(cdt, cdn, "rate_in_uom", row.basic_rate)
                }
            }
        })
    ])
}

frappe.ui.form.on("Stock Entry Detail", {
    // custom_quantity: function (frm, cdt, cdn) {
    //     var row = locals[cdt][cdn]
    //     frappe.run_serially([
    //         () => frappe.timeout(2),
    //         () => frappe.model.set_value(cdt, cdn, "qty", row.custom_quantity),
    //     ]);
    // },
    item_code: function (frm, cdt, cdn) {
        update_uom_rate(cdt,cdn)
    },
    basic_rate: function (frm, cdt, cdn) {
        update_uom_rate(cdt, cdn)
    }
})
