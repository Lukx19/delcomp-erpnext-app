// Copyright (c) 2016, Lukas Jelinek and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Worker Summary"] = {
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
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname": "task",
			"label": __("Task"),
			"fieldtype": "Link",
			"options": "Task",
			"get_query": function () {
				let project = frappe.query_report.get_filter_value('project');
				if (!project) {
					frappe.throw(__("Please select Project first"));
				}
				return {
					"filters": {
						"project": ["in", project],
					}
				}
			}

		}
	]
}
