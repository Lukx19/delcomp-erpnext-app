frappe.provide("erpnext");

erpnext.show_serial_batch_selector = function (frm, d, callback, on_close, show_dialog) {
	console.log("override");
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

frappe.provide("erpnext.stock");
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
	console.log("override");
	frappe.require("assets/delcomp/js/serial_no_batch_selector.js", function() {
		new delcomp.SerialNoBatchSelector({
			frm: frm,
			item: item,
			warehouse_details: get_warehouse_type_and_name(item),
		});
	});

}