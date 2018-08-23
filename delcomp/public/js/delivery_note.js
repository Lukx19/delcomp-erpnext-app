frappe.ui.form.on("Delivery Note", {
    onload: function () {
        // console.log("onload")
        frappe.call({
            method: "delcomp.delcomp.doctype.stock.overridejs_get_item_details",
            args: {},
            callback: function (r) { }
        });
    },
    resfresh: function () {
        // console.log("onload")
        frappe.call({
            method: "delcomp.delcomp.doctype.stock.overridejs_get_item_details",
            args: {},
            callback: function (r) {}
        });
    }
})
