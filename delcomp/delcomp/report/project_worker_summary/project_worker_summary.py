# Copyright (c) 2013, Lukas Jelinek and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
	if not filters:
		filters = {}
	elif filters.get("start_date") or filters.get("end_date"):
		filters["start_time"] = "00:00:00"
		filters["end_time"] = "24:00:00"

	columns = get_column()
	data = get_data(filters)
	return columns, data

def get_column():
	return [
		_("Project") + ":Link/Project:120",
		_("Task name") + "::150",
		_("Employee Name") + "::150",
		_("Payed to emp") + ":Currency:70",
		_("Time worked by emp") + ":Float:70",
	]

def get_timesheet_conditions(filters):
	conditions = " WHERE `tabTimesheet`.docstatus = 1"
	if filters.get("start_date"):
		conditions += " AND `tabTimesheet`.start_date >= timestamp(%(start_date)s, %(start_time)s)"
	if filters.get("end_date"):
		conditions += " AND `tabTimesheet`.end_date <= timestamp(%(end_date)s, %(end_time)s)"
	if filters.get("project"):
		conditions += " AND `tabTimesheet`.project = %(project)s"
	if filters.get("task"):
		conditions += " AND `tabTimesheet`.task = %(task)s"
	match_conditions = build_match_conditions("Timesheet")
	if match_conditions:
		conditions += " AND %s" % match_conditions
	return conditions

def get_data(filters):
	query = """
		WITH timesheet_data AS
			(SELECT
				`tabTimesheet`.project ,
				employee_name,
				task_name,
				task,
				SUM(`tabTimesheet`.total_billable_hours) as hours_per_emp,
				SUM(`tabTimesheet`.total_billable_amount) as pay_per_emp
			FROM `tabTimesheet`
			{timesheet_conds}
			GROUP BY project,employee,task)
		SELECT
			project,
			task_name,
			employee_name,
			pay_per_emp,
			hours_per_emp
		FROM timesheet_data
		ORDER BY project, task_name
		""".format(timesheet_conds=get_timesheet_conditions(filters))
	data = frappe.db.sql(query,filters,as_list=1)
	return data

