from __future__ import unicode_literals
from frappe.utils.data import nowdate, getdate,add_days,add_months
import frappe
import datetime
import dateutil.relativedelta

def execute():
	# if datetime.date.today()==datetime.date.today().replace(day=21):
	for emp in frappe.get_all('Employee'):
		total_cost_ot_1=0
		total_cost_ot_2=0
		sc1_row=[]
		sc2_row=[]
		overtime_list1=[]
		overtime_list2=[]
		fltr={'employee':emp.name}
		fltr.update({'date': ['between', [add_months(getdate(nowdate()),-1), add_days(getdate(nowdate()),-1)]]})
		for ov in frappe.get_all('Overtime Calculation',filters={'employee':emp.name},fields=['name','date','salary_component','overtime_period','overtime_cost']):
			if ov.get('salary_component')=='OT 1.5 Amt':
				sc1_row.append({
					'overtime_detail':ov.get('name'),
					'date':ov.get('date'),
					'overtime':ov.get('overtime_period')
				})
				total_cost_ot_1+=float(ov.get('overtime_cost'))
				overtime_list1.append(ov.get('overtime_period'))
			else:
				sc2_row.append({
					'overtime_detail':ov.get('name'),
					'date':ov.get('date'),
					'overtime':ov.get('overtime_period')
				})
				total_cost_ot_2+=float(ov.get('overtime_cost'))
				overtime_list2.append(ov.get('overtime_period'))

		if len(sc1_row)>0:
			as1=frappe.new_doc("Additional Salary")
			as1.employee=emp.name
			as1.salary_component='OT 1.5 Amt'
			as1.amount=total_cost_ot_1
			as1.total_overtime=calculate_total_overtime(overtime_list1)
			as1.payroll_date=datetime.date.today()
			for d in sc1_row:
				as1.append('overtime_details',d)
			as1.insert()

		if len(sc2_row)>0:
			as2=frappe.new_doc("Additional Salary")
			as2.employee=emp.name
			as2.salary_component='OT 2 Amt'
			as2.amount=total_cost_ot_2
			as2.total_overtime=calculate_total_overtime(overtime_list2)
			as2.payroll_date=datetime.date.today()
			for d in sc2_row:
				as2.append('overtime_details',d)
			as2.insert()

def calculate_total_overtime(ot_list):
	totalSecs = 0
	for tm in ot_list:
		timeParts = [int(s) for s in tm.split(':')]
		totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
	totalSecs, sec = divmod(totalSecs, 60)
	hr, min = divmod(totalSecs, 60)
	return ("%d:%02d:%02d" % (hr, min, sec))


def update_total(doc,method):
	sc=2
	if doc.salary_component=='OT 1.5 Amt':
		sc=1.5
	ov_list=[]
	for ov in doc.overtime_details:
		ov_list.append(ov.get('overtime'))
	doc.total_overtime=calculate_total_overtime(ov_list)
	from datetime import datetime, timedelta
	t = datetime.strptime(calculate_total_overtime(ov_list), '%H:%M:%S')
	delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
	doc.amount=(2*sc*(delta.seconds/60)*1.666)

