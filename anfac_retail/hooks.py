from . import __version__ as app_version

app_name = "anfac_retail"
app_title = "Anfac Retail"
app_publisher = "Anfac Tech"
app_description = "Anfac Retail"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "Info@anfactech.so"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/anfac_retail/css/anfac_retail.css"
app_include_js = "/assets/anfac_retail/js/anfac_retail.js"

# include js, css files in header of web template
# web_include_css = "/assets/anfac_retail/css/anfac_retail.css"
# web_include_js = "/assets/anfac_retail/js/anfac_retail.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "anfac_retail/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"Sales Invoice": "public/js/sales_invoice.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {
# 	"Sales Invoice": "public/js/sales_invoice.js",

	
# 	}
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


# Custom Jinja Filters
# ----------
jenv = {
	"methods": [
		"format_value:anfac_retail.api.api.frappe_format_value"
	]
}

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "anfac_retail.install.before_install"
# after_install = "anfac_retail.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "anfac_retail.uninstall.before_uninstall"
# after_uninstall = "anfac_retail.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "anfac_retail.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Landed Cost Voucher" : {
	#	"on_submit" : "anfac_retail.api.land_cost_voucher.create_journal",
	#	"on_cancel" : "anfac_retail.api.land_cost_voucher.cancel_journal"
	},
	"Stock Reconciliation" : {
		"on_submit" : "anfac_retail.api.retail_settings.stock_reconciliation_retail",
	},
	"Purchase Invoice" : {
		# "on_submit" : "anfac_retail.api.retail_setup.purchase_invoice_retail",
	}
}
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"anfac_retail.tasks.all"
# 	],
# 	"daily": [
# 		"anfac_retail.tasks.daily"
# 	],
# 	"hourly": [
# 		"anfac_retail.tasks.hourly"
# 	],
# 	"weekly": [
# 		"anfac_retail.tasks.weekly"
# 	]
# 	"monthly": [
# 		"anfac_retail.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "anfac_retail.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "anfac_retail.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "anfac_retail.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"anfac_retail.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []


fixtures = [
    {"dt":"Custom Field", "filters": [["dt", "in", ("Customer", "Contact")], ["fieldname", "in", ("disable_customer_statements", "is_customer_statement_contact")]]}
]
