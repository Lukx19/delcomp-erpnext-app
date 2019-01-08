var show_dialog = function (frm) {
    if (frm.doc.ask_for_batch_number) {
        frappe.flags.hide_serial_batch_dialog = false
    } else {
        frappe.flags.hide_serial_batch_dialog = true
    }
}

var render_multiple_add = function (frm) {
    let grid = frm.get_field("items").grid
    grid.multiple_set = false
    let btn = $(grid.wrapper).find(".grid-add-multiple-rows");
    btn.off("click")
    if (frappe.flags.hide_serial_batch_dialog) {
        grid.set_multiple_add("item_code", "custom_quantity");
    } else {
        grid.set_multiple_add("item_code");
    }
}

var add_generate_batch_button = function (frm) {
    if (frm.doc.__islocal) {
        return;
    }
    if (frm.doc.purpose != "Material Receipt") {
        return;
    }
    var grid = frm.fields_dict.items.grid;
    grid.add_custom_button( __("Generate Batch Numbers"), function () {
        // console.log(grid);
        var dialog = new frappe.ui.Dialog({
			title: "Choose batch series code",
            fields: [
                {
                    fieldname: 'batch_no_code',
                    read_only: 0,
                    fieldtype:'Data',
                    label: __('Batch series code'),
                    default: "19/10/TOVAR/.####",
                    description:"Zadaný reťazec je v tvare rok/mesiac/názov tovaru/####. Zmeniť je možné všetky čacti okrem '.####'."
                }
            ]
        });

        dialog.set_primary_action(__('Generate'), function(data) {
            let formating_code = data.batch_no_code
             // check if batch with this name exists
            let item_codes = {};
            let item_count = 0;
            grid.get_data().forEach((row) => {
                if (row.hasOwnProperty("item_code") &&
                    (!row.hasOwnProperty("batch_no")
                    || (row.hasOwnProperty("batch_no") && row.batch_no == ""))) {
                    item_codes[row.name] = row.item_code;
                    item_count += 1;
                }
            });
            // console.log(item_codes)
            if (item_count == 0) {
                frappe.throw(__("You have zero items with empty batch number field. If you want to generate batch numbers you need to have empty batch number fields in the item table."));
            }else{
                frappe.call({
                    method: "delcomp.delcomp.api.create_batch_entries",
                    args: {
                        item_codes: item_codes,
                        batch_number_series: formating_code,
                        doctype: frm.doctype,
                        doctype_name: frm.docname
                    },
                    callback: function (r) {
                        if (!r.message) {
                            return
                        }
                        // console.log(r.message);
                        r.message.forEach(row => {
                            frappe.model.set_value(grid.doctype, row[0], "batch_no", row[2])
                        });

                     }
                });
            }
            dialog.hide();

        });

        dialog.show();
    });
}

frappe.ui.form.on("Stock Entry", {
    onload_post_render: function (frm) {
        show_dialog(frm);
        render_multiple_add(frm);

        if (frm.doc.__islocal) {
            frm.fields_dict.items.grid.remove_all();
            frm.refresh_field("items");
        }

    },

    onload: function (frm) {
        add_generate_batch_button(frm);
    },

    refresh: function (frm) {
        add_generate_batch_button(frm);
    },

    ask_for_batch_number: function (frm) {
        show_dialog(frm);
        render_multiple_add(frm);
    }

})

frappe.ui.form.on("Stock Entry Detail", {
    custom_quantity: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        frappe.run_serially([
            () => frappe.timeout(2),
            () => frappe.model.set_value(cdt, cdn, "qty", row.custom_quantity),
            () => frappe.model.trigger("qty",row.custom_quantity, row),
        ]);
    },
    item_code: function (frm, cdt, cdn) {
        update_uom_rate(cdt, cdn, "basic_rate");
    },
    basic_rate: function (frm, cdt, cdn) {
        update_uom_rate(cdt, cdn, "basic_rate");
    }
})
