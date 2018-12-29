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