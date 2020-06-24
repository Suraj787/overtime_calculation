from __future__ import unicode_literals
from frappe.utils.data import nowdate, getdate,add_days
import frappe

def execute(doc,method):
	if doc.get("__islocal") and doc.log_type=='OUT':
		from datetime import datetime
		checkout=datetime.strptime(doc.time, "%Y-%m-%d %H:%M:%S")
		checkin=''
		if doc.shift=='Daytime':
			for ch_in in frappe.db.sql("""select time from `tabEmployee Checkin` where employee='{0}' and log_type='IN' and date(time)='{1}' and shift='{2}' order by time limit 1""".format(doc.employee,getdate(checkout),doc.shift),as_dict=1):
				checkin=ch_in.get('time')
		if doc.shift=='Night Shift':
			checkout=doc.time
			for ch_in in frappe.db.sql("""select time from `tabEmployee Checkin` where employee='{0}' and log_type='IN' and date(time)='{1}' and shift='{2}' order by time limit 1""".format(doc.employee,getdate(add_days(checkout,-1)),doc.shift),as_dict=1):
				checkin=ch_in.get('time')
		if checkout and checkin and doc.shift:
			start,end=frappe.db.get_value('Shift Type',doc.shift,['start_time','end_time'])
			actual_working_hr=checkout-checkin
			standard_working_hr=end-start
			duration=(actual_working_hr-standard_working_hr)
			seconds = duration.total_seconds()
			hours = seconds / 3600
			if hours>=float(1):
				holidays=[]
				holiday_list,department=frappe.db.get_value('Employee',doc.employee,['holiday_list','department'])
				for hl in frappe.get_all('Holiday',filters={'parent':holiday_list},fields=['holiday_date']):
					holidays.append(hl.get('holiday_date'))
				salary_component='OT 1.5 Amt'
				sc=1.5
				import datetime
				if datetime.date.today() in holidays:
					salary_component='OT 2 Amt'
					sc=2
				if standard_working_hr < actual_working_hr :
					oc=frappe.new_doc("Overtime Calculation")
					oc.date=datetime.date.today()
					oc.holiday_list=holiday_list
					oc.employee=doc.employee
					oc.salary_component=salary_component
					oc.department=department
					oc.shift=doc.shift
					oc.checkin=checkin.time()
					oc.checkout=checkout.time()
					oc.shift_start_time=start
					oc.shift_end_time=end
					oc.overtime_period=duration
					oc.actual_working_time=actual_working_hr
					oc.standard_working_period=standard_working_hr
					oc.overtime_cost=2*sc*((duration).seconds/60)*1.666
					oc.insert()
					oc.submit()
