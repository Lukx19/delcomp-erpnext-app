var update_uom_rate = function (cdt, cdn,rate_fieldname) {
    var row = locals[cdt][cdn]
    if (!row.item_code)
        return

    frappe.db.get_value('Item', { item_code: row.item_code }, 'price_uom').then(rdb => {
        const uom = rdb.message.price_uom;
        frappe.run_serially([
            () => frappe.timeout(2),
            () => frappe.call({
                method: "erpnext.stock.get_item_details.get_conversion_factor",
                args: {
                    item_code: row.item_code,
                    uom: uom
                },
                callback: function (r) {
                    if (!r.message)
                        return;
                    var conversion = r.message.conversion_factor;
                    let price = flt(row[rate_fieldname]);
                    if (conversion) {
                        price = flt(price * conversion);
                    }

                    frappe.model.set_value(cdt, cdn, "rate_in_uom",
                        price.toFixed(2).toString() + "/" + uom);
                }
            })
        ])
    });
}

//  overrides original batch and serial selector
erpnext.stock.select_batch_and_serial_no = (frm, item) => {
	let get_warehouse_type_and_name = (item) => {
		let value = '';
		if(frm.fields_dict.from_warehouse.disp_status === "Write") {
			value = cstr(item.s_warehouse) || '';
			return {
				type: 'Source Warehouse',
				name: value
			};
		} else {
			value = cstr(item.t_warehouse) || '';
			return {
				type: 'Target Warehouse',
				name: value
			};
		}
	}

	if(item && item.has_serial_no
		&& frm.doc.purpose === 'Material Receipt') {
		return;
	}

	frappe.require("assets/delcomp/js/serial_no_batch_selector.js", function() {
		new delcomp.SerialNoBatchSelector({
			frm: frm,
			item: item,
			warehouse_details: get_warehouse_type_and_name(item),
		});
	});

}

erpnext.show_serial_batch_selector = function(frm, d, callback, on_close, show_dialog) {
	frappe.require("assets/delcomp/js/serial_no_batch_selector.js", function() {
		new delcomp.SerialNoBatchSelector({
			frm: frm,
			item: d,
			warehouse_details: {
				type: "Warehouse",
				name: d.warehouse
			},
			callback: callback,
			on_close: on_close
		}, show_dialog);
	});
}