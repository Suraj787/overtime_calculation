from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Overtime"),
			"items": [
				{
					"type": "doctype",
					"name": "Overtime",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Overtime Application",
				},
			]
		},
	]
