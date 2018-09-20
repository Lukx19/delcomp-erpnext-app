# Copyright (c) 2013, Lukas Jelinek and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions
from delcomp.delcomp.utils import combine_conditions

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
		_("Start Date") + "::120",
		_("Employee Name") + "::150",
		_("Total Hours") + ":Float:120",
		_("Total Amount") + ":Currency:120",
	]

def get_timesheet_conditions(filters):
	conditions = ""
	if filters.get("start_date"):
		conditions = combine_conditions(conditions,"`tabTimesheet`.start_date >= timestamp(%(start_date)s, %(start_time)s)")
	if filters.get("end_date"):
		conditions = combine_conditions(conditions," `tabTimesheet`.end_date <= timestamp(%(end_date)s, %(end_time)s)")
	if filters.get("employee"):
		conditions = combine_conditions(conditions,"`tabTimesheet`.employee = %(employee)s")
	if filters.get("project"):
		conditions = combine_conditions(conditions,"`tabTimesheet`.project = %(project)s")
	if filters.get("task"):
		conditions = combine_conditions(conditions,"`tabTimesheet`.task = %(task)s")
	match_conditions = build_match_conditions("Timesheet")
	if match_conditions:
		conditions = combine_conditions(conditions,"%s" % match_conditions)
	return conditions


def get_data(filters):
	query = """
		SELECT
		    start_date,
			employee_name,
			SUM(`tabTimesheet`.total_billable_hours) as hours_per_emp,
			SUM(`tabTimesheet`.total_billable_amount) as pay_per_emp
		FROM `tabTimesheet`
		{timesheet_conds}
		GROUP BY start_date,employee
		ORDER BY start_date, employee
		""".format(timesheet_conds=get_timesheet_conditions(filters))
	data = frappe.db.sql(query,filters,as_list=1)
	return data

