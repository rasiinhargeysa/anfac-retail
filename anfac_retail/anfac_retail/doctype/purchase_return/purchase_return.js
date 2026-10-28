// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// attach required files
{% include 'erpnext/public/js/controllers/buying.js' %};

erpnext.buying.SupplierQuotationController = class SupplierQuotationController extends erpnext.buying.BuyingController {
	setup() {
		this.frm.custom_make_buttons = {
			'Purchase Order': 'Purchase Order',
			'Quotation': 'Quotation'
		}

		super.setup();
	}

	make_purchase_order() {
		frappe.model.open_mapped_doc({
			method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
			frm: cur_frm
		})
	}
	make_quotation() {
		frappe.model.open_mapped_doc({
			method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_quotation",
			frm: cur_frm
		})

	}
};

// for backward compatibility: combine new and previous states
extend_cscript(cur_frm.cscript, new erpnext.buying.SupplierQuotationController({frm: cur_frm}));

cur_frm.fields_dict['items'].grid.get_field('project').get_query =
	function(doc, cdt, cdn) {
		return{
			filters:[
				['Project', 'status', 'not in', 'Completed, Cancelled']
			]
		}
	}
frappe.ui.form.on('Purchase Return', {
	refresh: function(frm) {
		if(frm.is_new()){
			// alert('ok')
			frm.set_value("purchase_invoice" , '')
		}
	},
		supplier: function(frm){
			frappe.call({
				method: "erpnext.accounts.utils.get_balance_on",
				args: {
					company: frappe.defaults.get_user_default("Company"),
					party_type: "Supplier",
					party: frm.doc.supplier,
					date: frappe.datetime.get_today()
				},
				callback: function(r, rt) {
					if(r.message) {
						// alert(r.message)
					frm.set_value("supplier_balance", r.message)
					}
				}
			});
			retrun
		},
		details: function(frm){
		   frappe.call({
				method: "anfac_retail.api.api.get_report_content_2",
				args: {
				  
				  company: frappe.defaults.get_default('Company'),
				  supplier_name: frm.doc.supplier,
				  from_date: "01-01-2020",
				  to_date: frappe.datetime.nowdate()
				},
				callback: function (r) {
				  
				  var x = window.open();
				  x.document.open().write(r.message);
				}
			  });
		},	
		
	})



frappe.ui.form.on('Purchase Return Item', {
	amount: function(frm , cdt , cdn){
		let row = locals[cdt][cdn]
		row.rate = row.amount/row.qty
		if(row.qty){
		frm.refresh_field('items')
		}
	   // console.log(row)
	   // alert("ok")
		},
})