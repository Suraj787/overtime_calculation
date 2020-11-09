import frappe
from frappe.utils import flt, nowdate, getdate, add_days,today
def execute(doc,method):
	holidayDoc={'holidays':[]}
	emp_doc=frappe.get_doc('Employee',doc.employee)
	if emp_doc.get('holiday_list'):
		holidayDoc=frappe.get_doc('Holiday List',emp_doc.get('holiday_list'))
	holidayList=[]
	for d in holidayDoc.get('holidays'):
		holidayList.append(d.holiday_date)
	if doc.status=='Absent' and getdate(doc.attendance_date) not in holidayList:
		lapp=frappe.new_doc('Leave Application')
		lapp.employee=doc.employee
		lapp.from_date=doc.attendance_date
		lapp.to_date=doc.attendance_date
		lapp.leave_type="Leave Without Pay"
		lapp.description="On Leave"
		lapp.save()
		lapp.status='Approved'
		for d in frappe.get_doc('Department',doc.department).get('leave_approvers'):
			lapp.leave_approver=d.approver
			break
		lapp.submit()
