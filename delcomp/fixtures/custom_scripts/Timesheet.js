var getRow = function (frm) {
  var rows = 0
  $.each(frm.doc.time_logs, function (i, d) {
    rows = rows + 1
  });
  var row
  if (rows == 0)
    row = frm.add_child("time_logs")
  else
    row = frm.doc.time_logs[0]
  return row
}


frappe.ui.form.on("Timesheet", {
  setup: function (frm) {
    console.log("setup")
    frm.fields_dict['project'].get_query = function () {
      return {
        filters: {
          'company': frm.doc.company,
          'status': ["=", "Open"]
        }
      }
    }

    frm.fields_dict['task'].get_query = function () {
      return {
        filters: {
          'project': frm.doc.project
        }
      }
    }
  },


  onload: function (frm) {
    console.log("onload")
    if (frm.doc.end_date && frm.doc.start_date && frm.doc.__islocal) {
      frm.set_value("from_date", frm.doc.start_date);
      frm.set_value("to_date", frm.doc.end_date);
    }
  },
  from_date: function (frm) {
    var row = getRow(frm)
    console.log("row in from date", row.name)

    frappe.model.set_value(row.doctype, row.name, "from_time", frm.doc.from_date)
    if (!frm.doc.to_date && !frm.doc.end_date) {
      frm.set_value("to_date", frm.doc.from_date);
      frappe.model.set_value(row.doctype, row.name, "to_time", frm.doc.to_date)
    }
    var hours = moment(frm.doc.to_date).diff(moment(frm.doc.from_date), "seconds") / 3600
    frappe.model.set_value(row.doctype, row.name, "hours", hours)
    frm.refresh_field("time_logs")
  },

  to_date: function (frm) {
    var row = getRow(frm)
    frappe.model.set_value(row.doctype, row.name, "to_time", frm.doc.to_date)
    if (!frm.doc.from_date && !frm.doc.start_date) {
      frm.set_value("from_date", frm.doc.to_date);
      frappe.model.set_value(row.doctype, row.name, "from_time", frm.doc.from_date)
    }
    var hours = moment(frm.doc.to_date).diff(moment(frm.doc.from_date), "seconds") / 3600
    frappe.model.set_value(row.doctype, row.name, "hours", hours)
    frm.refresh_field("time_logs")
  },

  project: function (frm) {
    var row = getRow(frm)
    frappe.model.set_value(row.doctype, row.name, "project", frm.doc.project)
    frm.refresh_field("time_logs")
  },

  activity: function (frm) {
    var row = getRow(frm)
    frappe.model.set_value(row.doctype, row.name, "activity_type", frm.doc.activity)
    frm.refresh_field("time_logs")
  },

  task: function (frm) {
    var row = getRow(frm)
    frappe.model.set_value(row.doctype, row.name, "task", frm.doc.task)
    frm.refresh_field("time_logs")
  },

  refresh: function (frm) {
    console.log("refresh")
    var row = getRow(frm)
    frappe.model.set_value(row.doctype, row.name, "project", frm.doc.project)
    frappe.model.set_value(row.doctype, row.name, "task", frm.doc.task)
    frappe.model.set_value(row.doctype, row.name, "activity_type", frm.doc.activity)
    frappe.model.set_value(row.doctype, row.name, "from_time", frm.doc.from_date)
    frappe.model.set_value(row.doctype, row.name, "to_time", frm.doc.to_date)
    var hours = moment(frm.doc.to_date).diff(moment(frm.doc.from_date), "seconds") / 3600
    frappe.model.set_value(row.doctype, row.name, "hours", hours)
    frm.refresh_field("time_logs")
  },
  validate: function (frm) {
    console.log("validate")
    // console.log("validate", row.hours)
    // var row = getRow(frm)
    // frappe.model.set_value(row.doctype, row.name, "project", frm.doc.project)
    // frappe.model.set_value(row.doctype, row.name, "task", frm.doc.task)
    // frappe.model.set_value(row.doctype, row.name, "activity_type", frm.doc.activity)
    // frappe.model.set_value(row.doctype, row.name, "from_time", frm.doc.from_date)
    // frappe.model.set_value(row.doctype, row.name, "to_time", frm.doc.to_date)
    // var hours = moment(frm.doc.to_date).diff(moment(frm.doc.from_date), "seconds") / 3600
    // frappe.model.set_value(row.doctype, row.name, "hours", hours)
    // frm.refresh_field("time_logs")
    // return true
  }
});
