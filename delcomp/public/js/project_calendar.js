frappe.views.calendar["Project"] = {
    field_map: {
        "start": "expected_start_date",
        "end": "expected_end_date",
        "name": "name",
        "id": "name",
        "allDay": "allDay",
        "child_name": "name",
        "title": "name",
        "tooltip": "name",
        "status": "status",
    },
    style_map: {
        "Open": "info",
        "Completed": "standard",
        "Canceled": "danger"
    },
    color_map: {
        red: "red",
        yellow: "yellow",
        green: "green",
    },
    // get_css_class: function (doc) {
    //     let map = {
    //         "Open":  "green",
    //         "Completed": "yellow",
    //         "Canceled": "red"
    //     }
    //     return map[doc.status]
    // },
    gantt: false,
    filters: [
        {
            "fieldtype": "Link",
            "fieldname": "project",
            "options": "Project",
            "label": __("Project")
        },
    ],
    // get_events_method: "delcomp.delcomp.doctype.project.get_events"
}
