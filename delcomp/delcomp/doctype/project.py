import frappe
from erpnext.projects.doctype.project.project import Project
from frappe.utils import getdate

def is_row_updated(self, row, existing_task_data):
	if self.get("__islocal") or not existing_task_data:
		return True

	d = existing_task_data.get(row.task_id)
	if not d:
		return False
	if (row.title != d.title or row.status != d.status
		or getdate(row.start_date) != getdate(d.start_date) or getdate(row.end_date) != getdate(d.end_date)
		or row.description != d.description or row.task_weight != d.task_weight):
		return True

	# check custom fields for changes
	project_task_custom_fields = frappe.get_all("Custom Field", {"dt": "Project Task"}, "fieldname")

	for field in project_task_custom_fields:
		if row.get(field.fieldname) != d.get(field.fieldname):
			return True


def override(doc, method):
	Project.is_row_updated = is_row_updated
