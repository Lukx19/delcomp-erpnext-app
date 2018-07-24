frappe.views.calendar["Timesheet"] = {
    field_map: {
        "start": "from_date",
        "end": "to_date",
        "name": "parent",
        "id": "name",
        "allDay": "allDay",
        "child_name": "name",
        "title": "title"
    },
    style_map: {
        "0": "info",
        "1": "standard",
        "2": "danger"
    },
    gantt: false,
    filters: [
        {
            "fieldtype": "Link",
            "fieldname": "project",
            "options": "Project",
            "label": __("Project")
        },
        {
            "fieldtype": "Link",
            "fieldname": "employee",
            "options": "Employee",
            "label": __("Employee")
        }
    ],
    get_events_method: "delcomp.delcomp.timesheet.timesheet.get_events"
}
