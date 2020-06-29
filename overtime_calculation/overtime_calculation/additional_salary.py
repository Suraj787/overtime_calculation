from __future__ import unicode_literals
from frappe.utils.data import nowdate, getdate,add_days,add_months
import frappe
import datetime
import dateutil.relativedelta

def execute():
	if datetime.date.today()==datetime.date.today().replace(day=21):
		for emp in frappe.get_all('Employee'):
			amount1=0
			amount2=0
			total1_hr=0
			total2_hr=0
			sc1_row=[]
			sc2_row=[]
			fltr={'employee':emp.name}
			fltr.update({'overtime_date': ['between', [add_months(getdate(nowdate()),-1), add_days(getdate(nowdate()),-1)]]})
			holidays=[]
			holiday_list,department,rate=frappe.db.get_value('Employee',emp.name,['holiday_list','department','hourly_overtime_rate_'])
			for hl in frappe.get_all('Holiday',filters={'parent':holiday_list},fields=['holiday_date']):
				holidays.append(hl.get('holiday_date'))
			for ov in frappe.get_all('Overtime Application',filters={'employee':emp.name},fields=['name','employee','employee_name','overtime','overtime_date']):
				overtime_hr=frappe.db.get_value('Overtime',{'name':ov.get('overtime')},'hours')
				salary_component='OT 1.5 Amt'
				sc=1.5
				if ov.overtime_date in holidays:
					salary_component='OT 2 Amt'
					sc=2
				if salary_component=='OT 1.5 Amt':
					sc1_row.append({
						'overtime_application':ov.get('name'),
						'date':ov.get('overtime_date'),
						'overtime':overtime_hr
					})
					amount1+=float(overtime_hr)*float(rate)*1.5
					total1_hr+=float(overtime_hr)
				else:
					sc2_row.append({
						'overtime_application':ov.get('name'),
						'date':ov.get('overtime_date'),
						'overtime':overtime_hr
					})
					amount2+=float(overtime_hr)*float(rate)*2
					total2_hr+=float(overtime_hr)

			if len(sc1_row)>0:
				as1=frappe.new_doc("Additional Salary")
				as1.employee=emp.name
				as1.salary_component='OT 1.5 Amt'
				as1.amount=amount1
				as1.payroll_date=datetime.date.today()
				as1.total_overtime=total1_hr
				for d in sc1_row:
					as1.append('overtime_details',d)
				as1.insert()

			if len(sc2_row)>0:
				as2=frappe.new_doc("Additional Salary")
				as2.employee=emp.name
				as2.salary_component='OT 2 Amt'
				as2.amount=amount2
				as2.payroll_date=datetime.date.today()
				as2.total_overtime=total2_hr
				for d in sc2_row:
					as2.append('overtime_details',d)
				as2.insert()
