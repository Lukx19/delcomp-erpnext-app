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