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
		_("Budget") + ":Currency:70",
		_("Bonus") + ":Currency:70",
		_("Payed to emp") + ":Currency:70",
		_("Time worked by emp") + ":Float:70",
		_("Work hours in task") + ":Float:70",
		_("Bonus based on work hours") + ":Currency:15"
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

def combine_conditions(conditions):
	if conditions == "":
		conditions += "WHERE"
	else:
		conditions += "AND"
	return conditions

def get_task_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions += combine_conditions(conditions)
		conditions += " `tabTask`.project = %(project)s"
	if filters.get("task"):
		conditions += combine_conditions(conditions)
		conditions += " `tabTimesheet`.name = %(task)s"
	match_conditions = build_match_conditions("Task")
	if match_conditions:
		conditions += combine_conditions(conditions)
		conditions += " %s" % match_conditions

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
			GROUP BY project,employee,task),
		task_budget AS
		 	(SELECT
			 	budget,
			 	`tabTask`.name
			 FROM `tabTask`
			 {task_conds}),
		task_totals AS
			(SELECT
				task,
				SUM(total_billable_hours) AS total_billing_hours,
				SUM(total_billable_amount) AS total_billing_amount
			FROM `tabTimesheet`
			{timesheet_conds}
			GROUP BY task),
  		task_data AS
			(SELECT *
			FROM task_budget
			JOIN task_totals ON  task_budget.name = task_totals.task)
  		SELECT
			project,
			task_name,
			employee_name,
			budget,
			(budget - total_billing_amount) as bonus,
			pay_per_emp,
			hours_per_emp,
			total_billing_hours,
			ROUND((budget - total_billing_amount) * (hours_per_emp/total_billing_hours),3) AS bonus_based_on_hours
		FROM timesheet_data
		JOIN task_data ON timesheet_data.task = task_data.task
		ORDER BY project, task_name
		""".format(timesheet_conds=get_timesheet_conditions(filters), task_conds= get_task_conditions(filters))
	data = frappe.db.sql(query,filters,as_list=1)
	return data
