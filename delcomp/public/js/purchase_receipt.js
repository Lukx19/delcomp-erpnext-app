frappe.ui.form.on("Purchase Receipt", {
    onload: function (frm) {
        console.log("onload")
        frappe.call({
            method: "delcomp.delcomp.doctype.stock.overridejs_get_item_details",
            args: {},
            callback: function (r) { }
        });


        if (frm.doc.__islocal) {
            frm.fields_dict.items.grid.remove_all();
            frm.refresh_field("items");
        }
    },
    setup: function () {
        console.log("setup")
        frappe.call({
            method: "delcomp.delcomp.doctype.stock.overridejs_get_item_details",
            args: {},
            callback: function (r) { }
        });
    },
    refresh: function () {
        console.log("refresh")
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
    }
})

frappe.ui.form.on("Purchase Receipt Item", {
    custom_quantity: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        frappe.run_serially([
            () => frappe.timeout(2),
            () => frappe.model.set_value(cdt, cdn, "qty", row.custom_quantity),
            () => frappe.model.set_value(cdt, cdn, "received_qty", row.custom_quantity),
            () => frappe.model.trigger("qty",row.custom_quantity, row),
        ])
    },

    item_code: function (frm,cdt, cdn) {
        update_uom_rate(cdt, cdn, "base_rate");

    },
    price_list_rate: function (frm,cdt, cdn) {
        update_uom_rate(cdt, cdn, "base_rate");
    }
})
