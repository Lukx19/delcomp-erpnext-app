frappe.ui.form.on("Purchase Receipt", {
    onload: function () {
        // console.log("setup")
        frappe.call({
            method: "delcomp.delcomp.doctype.stock.overridejs_get_item_details",
            args: {},
            callback: function (r) {}
        });
    }
})
