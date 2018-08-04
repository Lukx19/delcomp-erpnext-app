// Copyright (c) 2016, Lukas Jelinek and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Summary"] = {
	"filters": [
		{
            "fieldname": "start_date",
            "label": __("From Date"),
            "fieldtype": "Date",
			"default": frappe.datetime.year_start()
        },
        {
            "fieldname": "end_date",
            "label": __("To Date"),
            "fieldtype": "Date",
			"default": frappe.datetime.year_end()
        },
	]
}
