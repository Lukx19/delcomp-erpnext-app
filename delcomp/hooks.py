# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "delcomp"
app_title = "Delcomp"
app_publisher = "Lukas Jelinek"
app_description = "Erpnext changes for Delcomp,s.r.o."
app_icon = "octicon octicon-file-directory"
app_color = "brown"
app_email = "lukx19@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "assets/css/delcomp.min.css"
app_include_js = ["assets/js/delcomp.min.js"]

# include js, css files in header of web template
# web_include_css = "/assets/delcomp/css/delcomp.css"
# web_include_js = "/assets/delcomp/js/delcomp.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Timesheet" : "public/js/timesheet.js"}
doctype_list_js = {
					"Timesheet": "public/js/timesheet_list.js"
					}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {
						"Timesheet": "public/js/timesheet_calendar.js",
						"Project": "public/js/project_calendar.js"
						}

# "Custom DocPerm" , "Custom Script"
# -----------
fixtures = ["Role"]

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "delcomp.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "delcomp.install.before_install"
# after_install = "delcomp.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "delcomp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Timesheet": {
		# "validate": "delcomp.delcomp.timesheet.timesheet.printState",
		"after_save":"delcomp.delcomp.timesheet.timesheet.printState" ,
		# "on_update": "delcomp.delcomp.timesheet.timesheet.printState",
		"on_submit": "delcomp.delcomp.timesheet.timesheet.printState",
		# "on_change": "delcomp.delcomp.timesheet.timesheet.printState",
		"before_save": [
			"delcomp.delcomp.timesheet.timesheet.validate",
			"delcomp.delcomp.timesheet.timesheet.printState"
			],
		"before_update_after_submit": [
			"delcomp.delcomp.timesheet.timesheet.validate_after_submit",
			"delcomp.delcomp.timesheet.timesheet.printState"
		],
	},
	"Project": {
		"onload": "delcomp.delcomp.doctype.project.override",
		"validate":"delcomp.delcomp.doctype.project.override",
	}
}
# doc_events = {
# 	"Timesheet": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"delcomp.tasks.all"
# 	],
# 	"daily": [
# 		"delcomp.tasks.daily"
# 	],
# 	"hourly": [
# 		"delcomp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"delcomp.tasks.weekly"
# 	]
# 	"monthly": [
# 		"delcomp.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "delcomp.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "delcomp.event.get_events"
# }

