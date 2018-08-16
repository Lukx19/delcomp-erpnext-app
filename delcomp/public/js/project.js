var render_contact=  function (frm, contact_field, contact_view) {
    frappe.call({
        "method": "frappe.client.get",
        args: {
            doctype: "Contact",
            name: frm.doc[contact_field]
        },
        callback: function (data) {
            $(frm.fields_dict[contact_view].wrapper)
                .html(frappe.render_template("delcomp_contact", { "contact": data.message }))
        }
    })
}

var update_contact = function (frm, contact_field, contact_view) {
    if (frm.doc[contact_field]) {
        render_contact(frm, contact_field, contact_view)
    } else {
        $(frm.fields_dict[contact_view].wrapper).html("")
    }
}
frappe.ui.form.on("Project", {
    refresh: function (frm) {
        update_contact(frm, "contact", "contact_view")
        update_contact(frm, "contact_2", "contact_2_view")
    },
    address: function (frm) {
        if (frm.doc.address) {
            frappe.call({
                method: 'frappe.contacts.doctype.address.address.get_address_display',
                args: {
                    "address_dict": frm.doc.address
                },
                callback: function (r) {
                    frm.set_value("address_view", r.message)
                }
            });
        } else {
            frm.set_value("address_view", "")
        }
    },
    contact: function (frm) {
        update_contact(frm, "contact", "contact_view")
    },
    contact_2: function (frm) {
        update_contact(frm, "contact_2", "contact_2_view")
    }
})
