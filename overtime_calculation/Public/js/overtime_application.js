frappe.ui.form.on('Overtime Application', {
	overtime:function(frm){
	   frappe.db.get_value('Overtime',{'name':frm.doc.overtime},['supervisor','from_time','to_time','date','supervisor_name','hours','description'])
			.then(({ message }) => {
				frm.set_value('supervisor',message.supervisor);
				frm.set_value('from_time',message.from_time);
				frm.set_value('to_time',message.to_time);
				frm.set_value('overtime_date',message.date);
				frm.set_value('supervisor_name',message.supervisor_name);
				frm.set_value('hours',message.hours);
				frm.set_value('description',message.description);
			});
	},
	employee:function(frm){
  		frappe.db.get_value('Employee',{'name':frm.doc.employee},['designation','department','employee_name'])
		.then(({ message }) => {
			frm.set_value('employee_name',message.employee_name);
			frm.set_value('designation',message.designation);
            frm.set_value('department',message.department);
		});  
	}
})
