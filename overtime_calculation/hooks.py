# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "overtime_calculation"
app_title = "Overtime Calculation"
app_publisher = "bizmap tech"
app_description = "Overtime Calculation"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "suraj@bizmap.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/overtime_calculation/css/overtime_calculation.css"
# app_include_js = "/assets/overtime_calculation/js/overtime_calculation.js"

# include js, css files in header of web template
# web_include_css = "/assets/overtime_calculation/css/overtime_calculation.css"
# web_include_js = "/assets/overtime_calculation/js/overtime_calculation.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "overtime_calculation.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "overtime_calculation.install.before_install"
# after_install = "overtime_calculation.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "overtime_calculation.notifications.get_notification_config"

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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
# 
scheduler_events = {
	"daily": [
		"overtime_calculation.overtime_calculation.additional_salary.execute",
	]
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"overtime_calculation.tasks.all"
# 	],
# 	"daily": [
# 		"overtime_calculation.tasks.daily"
# 	],
# 	"hourly": [
# 		"overtime_calculation.tasks.hourly"
# 	],
# 	"weekly": [
# 		"overtime_calculation.tasks.weekly"
# 	]
# 	"monthly": [
# 		"overtime_calculation.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "overtime_calculation.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "overtime_calculation.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "overtime_calculation.task.get_dashboard_data"
# }

