frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		if (frm.is_new()) {
			frappe.call({
				method: "anfac_retail.api.get_last_doc.get_last_doc",
				args: { 
				  doc: "Sales Invoice"
				},
				callback: function(r) {
					var m = r.message
					var inv_n = m.toString();
					var inv_name = inv_n.replace(/\d/g, "");
					var res = parseInt(inv_n.replace(/\D/g, ""));
					if (res !== 1){
						frm.set_value("voucher_no" , `${inv_name}${res+1}` )
					}
					
				  
				}
			  });
		
	}
	}
})


frappe.ui.form.on('Sales Invoice Item', {
	refresh(frm) {
		// your code here
	},
	amount: function(frm , cdt , cdn){
	    let row = locals[cdt][cdn]
	    row.rate = row.amount/row.qty
	    if(row.qty){
	    frm.refresh_field('items')
	    }
	   // console.log(row)
	   // alert("ok")
	}
})



frappe.ui.form.on('Journal Entry', {
	refresh(frm) {
		if (frm.is_new()) {
			frappe.call({
				method: "anfac_retail.api.get_last_doc.get_last_doc",
				args: { 
				  doc: "Journal Entry"
				},
				callback: function(r) {
					var m = r.message
					var inv_n = m.toString();
					var inv_name = inv_n.replace(/\d/g, "");
					var res = parseInt(inv_n.replace(/\D/g, ""));
					if (res !== 1){
						frm.set_value("voucher_no" , `${inv_name}${res+1}` )
					}
					
				  
				}
			  });
		
	}
	}
})


frappe.ui.form.on('Stock Entry', {
	refresh(frm) {
		if (frm.is_new()) {
			frappe.call({
				method: "anfac_retail.api.get_last_doc.get_last_doc",
				args: { 
				  doc: "Stock Entry"
				},
				callback: function(r) {
					var m = r.message
					var inv_n = m.toString();
					var inv_name = inv_n.replace(/\d/g, "");
					var res = parseInt(inv_n.replace(/\D/g, ""));
					if (res !== 1){
						frm.set_value("voucher_no" , `${inv_name}${res+1}` )
					}
					
				  
				}
			  });
		
	}
	}
})


