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

def timesheet_conditions(filters):
	conds = []
	conds.append("`tabTimesheet`.docstatus > 0")
	if filters.get("start_date"):
		conds.append("`tabTimesheet`.start_date >= timestamp(%(start_date)s, %(start_time)s)")
	if filters.get("end_date"):
		conds.append("`tabTimesheet`.end_date <= timestamp(%(end_date)s, %(end_time)s)")
	if filters.get("project"):
		conds.append( "`tabTimesheet`.project = %(project)s")
	if filters.get("task"):
		conds.append( " `tabTimesheet`.task = %(task)s")
	match_conditions = build_match_conditions("Timesheet")
	if match_conditions:
		conds.append("%s" % match_conditions)
	if len(conds):
		return "WHERE " + " AND ".join(conds)
	else:
		return ""

def task_conditions(filters):
	conds = []
	if filters.get("project"):
		conds.append("`tabTask`.project = %(project)s")
	if filters.get("task"):
		conds.append(" `tabTask`.name = %(task)s")
	if filters.get("start_date") and filters.get("end_date"):
		time_combs = """
					((`tabTask`.act_start_date <= timestamp(%(start_date)s, %(start_time)s)
						AND `tabTask`.act_end_date >= timestamp(%(end_date)s, %(end_time)s))
					OR (`tabTask`.act_start_date >= timestamp(%(start_date)s, %(start_time)s)
						AND `tabTask`.act_start_date <= timestamp(%(end_date)s, %(end_time)s))
					OR (`tabTask`.act_end_date >= timestamp(%(start_date)s, %(start_time)s)
						AND `tabTask`.act_end_date <= timestamp(%(end_date)s, %(end_time)s)))
					"""
		conds.append(time_combs)
	else:
		if filters.get("start_date"):
			conds.append("`tabTask`.act_end_date >= timestamp(%(start_date)s, %(start_time)s)")
		if filters.get("end_date"):
			conds.append("`tabTask`.act_start_date <= timestamp(%(end_date)s, %(end_time)s)")

	if len(conds):
		return "WHERE " + " AND ".join(conds)
	else:
		return ""


def final_conditions(filters):
	conds = []
	if filters.get("employee"):
		conds.append( "employee = %(employee)s")

	if len(conds):
		return "WHERE " + " AND ".join(conds)
	else:
		return ""

def selected_columns():
	columns = [
		"project",
		"task_name",
		"employee_name",
		"pay_per_emp",
		"hours_per_emp",
		# "total_billing_hours",

	]
	if "Project Master Manager" in frappe.get_roles(frappe.session.user):
		columns.extend([
			"budget",
			"bonus",
			"bonus_based_on_hours"
		])
	return ",".join(columns)

def get_column():
	columns = [
		_("Projekt") + ":Link/Project:120",
		_("Úloha") + "::150",
		_("Zamestnanec") + "::150",
		_("Plat") + ":Currency:50",
		_("Odpracované hodiny") + ":Float:50",
		# _("Work hours in task") + ":Float:70",
	]

	if "Project Master Manager" in frappe.get_roles(frappe.session.user):
		columns.extend([
		_("Budget") + ":Currency:50",
		_("Bonus") + ":Currency:50",
		_("Bonus/hod") + ":Currency:50"
		])
	return columns

def get_data(filters):
	query = """
		WITH timesheet_data AS
			(SELECT
				`tabTimesheet`.project ,
				employee,
				employee_name,
				task,
				SUM(`tabTimesheet`.total_billable_hours) as hours_per_emp,
				SUM(`tabTimesheet`.total_billable_amount) as pay_per_emp
			FROM `tabTimesheet`
			{timesheet_conds}
			GROUP BY project,employee,task),
		task_data AS
			(SELECT
				`tabTask`.name AS task,
				`tabTask`.budget AS budget,
				`tabTask`.subject AS task_name,
				SUM(IFNULL(total_billable_hours,0)) AS total_billing_hours,
				SUM(IFNULL(total_billable_amount,0)) AS total_billing_amount,
				(`tabTask`.budget - SUM(IFNULL(total_billable_amount,0))) AS bonus
			FROM `tabTask`
			LEFT JOIN `tabTimesheet` ON
				(`tabTimesheet`.task = `tabTask`.name AND `tabTimesheet`.docstatus > 0)
			{task_conds}
			GROUP BY task),
		final_data AS
			(SELECT
				project,
				task_name,
				employee,
				employee_name,
				budget,
				bonus,
				pay_per_emp,
				hours_per_emp,
				total_billing_hours,
				ROUND(bonus * (hours_per_emp/total_billing_hours),3) AS bonus_based_on_hours
			FROM timesheet_data
			JOIN task_data ON timesheet_data.task = task_data.task)
		SELECT
			{selected_columns}
			FROM final_data
			{final_conds}
			ORDER BY project, task_name
		""".format(selected_columns = selected_columns(),timesheet_conds=timesheet_conditions(filters), task_conds= task_conditions(filters),final_conds=final_conditions(filters))
	# frappe.errprint("kl")
	# frappe.errprint(query)
	data = frappe.db.sql(query,filters,as_list=1)
	return data

