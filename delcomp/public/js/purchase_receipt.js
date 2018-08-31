frappe.ui.form.on("Purchase Receipt", {
    onload: function () {
        // console.log("onload")
        frappe.call({
            method: "delcomp.delcomp.doctype.stock.overridejs_get_item_details",
            args: {},
            callback: function (r) { }
        });
    },
    refresh: function () {
        // console.log("setup")
        frappe.call({
            method: "delcomp.delcomp.doctype.stock.overridejs_get_item_details",
            args: {},
            callback: function (r) {}
        });
    },
    onload_post_render: function (frm) {
        var grid = frm.get_field("items").grid
        grid.multiple_set = false
        var btn = $(grid.wrapper).find(".grid-add-multiple-rows");
        btn.off("click")
        grid.set_multiple_add("item_code", "custom_quantity");
    },
})

frappe.ui.form.on("Purchase Receipt Item", {
    custom_quantity: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        frappe.run_serially([
            () => frappe.timeout(2),
            () => frappe.model.set_value(cdt, cdn, "received_qty", row.custom_quantity),
        ]);
    }
})
