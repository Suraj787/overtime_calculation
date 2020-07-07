frappe.ui.form.on('Overtime', {
	supervisor:function(frm){
  		frappe.db.get_value('Employee',{'name':frm.doc.supervisor},['designation','department','employee_name'])
		.then(({ message }) => {
			frm.set_value('supervisor_name',message.employee_name);
			frm.set_value('designation',message.designation);
            frm.set_value('department',message.department);
		});  
	}
})
