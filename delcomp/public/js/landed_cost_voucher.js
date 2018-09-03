frappe.ui.form.on("Landed Cost Item", {
    items_add: function (frm) {
        console.log(frm.doc.items)
    },
    item_code: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn]
        console.log(row)
    }

})


