from __future__ import unicode_literals
from frappe.utils.data import nowdate, getdate,add_days
import frappe
import datetime

def execute():
	for emp in frappe.get_all('Employee',fields=['name','default_shift','holiday_list','department']):
		shift=frappe.db.get_value('Shift Assignment',{'employee':emp.name},'shift_type')
		holidays=[]
		for hl in frappe.get_all('Holiday',filters={'parent':emp.get('holiday_list')},fields=['holiday_date']):
			holidays.append(hl.get('holiday_date'))
		if not shift:
			shift=emp.get('default_shift')

		# date=add_days(datetime.date.today(),-16)
		date=datetime.date.today()
		ch_in_detail={}
		ch_out_detail={}

		for ch_in in frappe.db.sql("""select employee,time,log_type,shift from `tabEmployee Checkin` where employee='{0}' and log_type='IN' and date(time)='{1}' order by time limit 1""".format(emp.name,date),as_dict=1):
			ch_in_detail.update(ch_in)
		for ch_out in frappe.db.sql("""select employee,time,log_type,shift from `tabEmployee Checkin` where employee='{0}' and log_type='OUT' and date(time)='{1}' order by time desc limit 1""".format(emp.name,date),as_dict=1):
			ch_out_detail.update(ch_out)

		if ch_in_detail and ch_out_detail and shift:
			start,end=frappe.db.get_value('Shift Type',shift,['start_time','end_time'])
			actual_working_hr=ch_out_detail.get('time')-ch_in_detail.get('time')
			standard_working_hr=end-start
			duration=(actual_working_hr-standard_working_hr)
			seconds = duration.total_seconds()
			hours = seconds / 3600
			if hours>=float(1):
				salary_component='OT 1.5 Amt'
				sc=1.5
				if date in holidays:
					salary_component='OT 2 Amt'
					sc=2

				if standard_working_hr < actual_working_hr :
					oc=frappe.new_doc("Overtime Calculation")
					oc.date=date
					oc.holiday_list=emp.get('holiday_list')
					oc.employee=emp.name
					oc.salary_component=salary_component
					oc.department=emp.get('department')
					oc.shift=shift
					oc.checkin=ch_in_detail.get('time').time()
					oc.checkout=ch_out_detail.get('time').time()
					oc.shift_start_time=start
					oc.shift_end_time=end
					oc.overtime_period=((actual_working_hr-standard_working_hr))
					oc.actual_working_time=actual_working_hr
					oc.standard_working_period=standard_working_hr
					oc.overtime_cost=2*sc*((actual_working_hr-standard_working_hr).seconds/60)*1.666
					oc.insert()
				
				


				