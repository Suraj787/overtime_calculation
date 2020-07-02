from __future__ import unicode_literals
from frappe.utils.data import nowdate, getdate,add_days,add_months
import frappe
import dateutil.relativedelta

def execute(doc,method):
	amount1=0
	amount2=0
	total1_hr=0
	total2_hr=0
	sc1_row=[]
	sc2_row=[]
	holidays=[]
	holiday_list,department,rate=frappe.db.get_value('Employee',doc.employee,['holiday_list','department','hourly_overtime_rate_'])
	from datetime import datetime
	for hl in frappe.get_all('Holiday',filters={'parent':holiday_list},fields=['holiday_date']):
		holidays.append(hl.get('holiday_date').strftime("%Y-%m-%d"))
	overtime_hr=frappe.db.get_value('Overtime',{'name':doc.get('overtime')},'hours')
	salary_component='OT 1.5 Amt'
	sc=1.5
	if doc.get('overtime_date') in holidays:
		salary_component='OT 2 Amt'
		sc=2
	if salary_component=='OT 1.5 Amt':
		sc1_row.append({
			'overtime_application':doc.get('name'),
			'date':doc.get('overtime_date'),
			'overtime':overtime_hr
		})
		amount1+=float(overtime_hr)*float(rate)*1.5
		total1_hr+=float(overtime_hr)
	else:
		sc2_row.append({
			'overtime_application':doc.get('name'),
			'date':doc.get('overtime_date'),
			'overtime':overtime_hr
		})
		amount2+=float(overtime_hr)*float(rate)*2
		total2_hr+=float(overtime_hr)

	if len(sc1_row)>0:
		as1=frappe.new_doc("Additional Salary")
		as1.employee=doc.employee
		as1.salary_component='OT 1.5 Amt'
		as1.amount=amount1
		as1.payroll_date=doc.get('overtime_date')
		as1.total_overtime=total1_hr
		for d in sc1_row:
			as1.append('overtime_details',d)
		as1.insert()

	if len(sc2_row)>0:
		as2=frappe.new_doc("Additional Salary")
		as2.employee=doc.employee
		as2.salary_component='OT 2 Amt'
		as2.amount=amount2
		as2.payroll_date=doc.get('overtime_date')
		as2.total_overtime=total2_hr
		for d in sc2_row:
			as2.append('overtime_details',d)
		as2.insert()