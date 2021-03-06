import frappe
import json

from frappe import _
from erpnext.controllers.queries import get_match_cond
from frappe.utils import flt, time_diff_in_hours, get_datetime, getdate, cint
from erpnext.projects.doctype.timesheet.timesheet import get_activity_cost

def validate(doc, method):
	# frappe.errprint("validate")
	latest = doc
	row = None
	if len(latest.time_logs) == 0:
		row = latest.append("time_logs",{})
	else:
		row = latest.time_logs[0]
	row.from_time = latest.from_date
	row.to_time = latest.to_date
	row.hours = time_diff_in_hours(row.to_time,row.from_time)
	row.project = latest.project
	row.task = latest.task
	row.activity_type = latest.activity

	if latest.billable:
		row.billable = True
		row.billing_hours = row.hours

	else:
		row.billable = False
		row.billing_hours = 0
	rate = get_activity_cost(doc.employee, doc.activity)
	row.billing_rate = rate.billing_rate
	row.costing_rate = rate.costing_rate
	latest.validate()

def update_billing_hours(doc, table):
	if doc.billable:
		if flt(table.billing_hours) == 0.0:
			table.billing_hours = table.hours
	else:
		table.billing_hours = 0

def update_billing_amount(doc, table):
	rate = get_activity_cost(doc.employee, doc.activity).billing_rate
	# frappe.errprint(str(doc.billable) + "  " +str(rate))
	if doc.billable:
		table.billing_amount = table.billing_hours * rate
	else:
		table.billing_amount = 0


def calculate_total_amounts(doc):
		doc.total_hours = 0.0
		doc.total_billable_hours = 0.0
		doc.total_billed_hours = 0.0
		doc.total_billable_amount = 0.0
		doc.total_costing_amount = 0.0
		doc.total_billed_amount = 0.0

		for d in doc.get("time_logs"):
			update_billing_hours(doc,d)
			update_billing_amount(doc,d)
			doc.total_hours += flt(d.hours)
			doc.total_costing_amount += flt(d.costing_amount)
			if d.billable:
				doc.total_billable_hours += flt(d.billing_hours)
				doc.total_billable_amount += flt(d.billing_amount)
				doc.total_billed_amount += flt(d.billing_amount) if d.sales_invoice else 0.0
				doc.total_billed_hours += flt(d.billing_hours) if d.sales_invoice else 0.0


def validate_after_submit(doc, method):
	# frappe.errprint("valid after submit custom")
	latest = doc
	calculate_total_amounts(latest)
	billable_hours =0
	if latest.billable:
		billable_hours =latest.total_billable_hours




@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.
	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	filters = json.loads(filters)
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Timesheet", filters)

	return frappe.db.sql(
		"""SELECT `tabTimesheet Detail`.name as name,
			`tabTimesheet Detail`.docstatus as status,
			`tabTimesheet Detail`.parent as parent,
			employee_name,
			`tabTimesheet`.from_date as from_date,
			`tabTimesheet`.total_hours as hours,
			activity,
			`tabTimesheet`.project,
			`tabTimesheet`.to_date as to_date,
			CONCAT(employee_name,' \n Projekt: ',`tabTimesheet`.project,'\n Aktivita: ',activity,' \n Úloha: ',`tabTimesheet`.task_name,'\n', ' (', ROUND(total_hours,2),' hrs)') as title
		FROM `tabTimesheet`, `tabTimesheet Detail`
		WHERE `tabTimesheet Detail`.parent = `tabTimesheet`.name
			AND `tabTimesheet`.docstatus < 2
			AND (from_date <= %(end)s and to_date >= %(start)s) {conditions} {match_cond}
		ORDER BY employee_name
		""".format(conditions=conditions, match_cond = get_match_cond('Timesheet')),
		{
			"start": start,
			"end": end
		}, as_dict=True, update={"allDay": 0})
