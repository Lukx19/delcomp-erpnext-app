frappe.ui.form.on("Task", {
    setup: function (frm) {
        frm.fields_dict['title_template'].get_query = function () {
            return {
                filters: {
                    'disabled': ["=", "False"]
                }
            }
        }
    },
    title_template: function (frm) {
        frm.add_fetch('title_template', 'title', 'subject')
    }
})
