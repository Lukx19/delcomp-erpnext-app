// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Status"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.year_start()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Item Group"
		},
		// {
		// 	"fieldname":"brand",
		// 	"label": __("Brand"),
		// 	"fieldtype": "Link",
		// 	"options": "Brand"
		// },
		{
			"fieldname": "item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Item",
			"get_query": function() {
				return {
					query: "delcomp.delcomp.doctype.queries.item_query"
				}
			},
			"filters": { "has_variants": 0 }
		},
		{
			"fieldname": "item_variant",
			"label": __("Variant"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Item",
			"get_query": function () {
				return {
					query: "delcomp.delcomp.doctype.queries.item_query"
				}
			},
			"filters": { "has_variants": 1 }
		}
		// {
		// 	"fieldname": "warehouse",
		// 	"label": __("Warehouse"),
		// 	"fieldtype": "Link",
		// 	"width": "80",
		// 	"options": "Warehouse"
		// },
		// {
		// 	"fieldname": "show_variant_attributes",
		// 	"label": __("Show Variant Attributes"),
		// 	"fieldtype": "Check"
		// },
	]
}
