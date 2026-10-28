

// $( "#purchase_detal_btn" ).click(function() {
//     alert( "Handler for .click() called." );
//   })

function consoleerp_hi(data , _from , to){
    // alert(data)
    // alert(_from)
    // alert(to)
	frappe.set_route('query-report', 'Purchase Items', { supplier: data , from_date : _from , to_date : to})
}

function sales_items(data , _from , to){
    // alert(data)
    // alert(_from)
    // alert(to)
	frappe.set_route('query-report', 'Sales Items', { customer: data , from_date : _from , to_date : to})
}


function statement(party){
    let d = new frappe.ui.Dialog({
        title: 'Enter details',
        fields: [
            {
                label: 'From Date',
                fieldname: 'from_date',
                fieldtype: 'Date',
                reqd : 1
            },
            {
                label: 'To Date',
                fieldname: 'to_date',
                fieldtype: 'Date',
                reqd : 1
            },
            
        ],
        primary_action_label: 'Submit',
        primary_action(values) {
            frappe.call({
                method: "anfac_retail.api.api.get_report_content",
                args: {
                  
                  company: frappe.defaults.get_default('Company'),
                  customer_name: party,
                  from_date: values.from_date,
                  to_date: values.to_date
                },
                callback: function (r) {
                  
                  var x = window.open();
                  x.document.open().write(r.message);
                }
              });
            d.hide();
        }
    });
    
    d.show();
    // alert(party)
    // frappe.new_doc("Customer Statements Sender"  ,{ customer: party } )
    // frappe.set_route('Form', 'Customer Setatements Sender',"Customer Statements Sender" ,{ customer: party })

}

function statementsuppier(party){
    let d = new frappe.ui.Dialog({
        title: 'Enter details',
        fields: [
            {
                label: 'From Date',
                fieldname: 'from_date',
                fieldtype: 'Date',
                reqd : 1
            },
            {
                label: 'To Date',
                fieldname: 'to_date',
                fieldtype: 'Date',
                reqd : 1
            },
            
        ],
        primary_action_label: 'Submit',
        primary_action(values) {
            frappe.call({
                method: "anfac_retail.api.api.get_report_content_2",
                args: {
                  
                  company: frappe.defaults.get_default('Company'),
                  supplier_name: party,
                  from_date: values.from_date,
                  to_date: values.to_date
                },
                callback: function (r) {
                  
                  var x = window.open();
                  x.document.open().write(r.message);
                }
              });
            d.hide();
        }
    });
    
    d.show();
    // alert(party)
    // frappe.new_doc("Customer Statements Sender"  ,{ customer: party } )
    // frappe.set_route('Form', 'Customer Setatements Sender',"Customer Statements Sender" ,{ customer: party })

}
// $( "#purchase_detal_btn").hide()

//   alert($("#purchase_detal_btn").text())
// alert("ok ok ok")

// frappe.views.Workspace = class customWorkspace {
//     constructor(wrapper) {
// 		this.wrapper = $(wrapper);
// 		this.page = wrapper.page;
//         this.prepare_container()
//     }
//     show() {
//         let body = `<h1> Dashboard  View Page</h1>`
//         $(frappe.render_template(frappe.render_template('erpnext/stock/page/warehouse_capacity_summary/warehouse_capacity_summary.html'), this)).appendTo(this.page.main)
//         // $(frappe.render_template(body, this)).appendTo(this.page.sidebar)
        
//         // this.page.add_inner_button(__("Create Workspace"), () => {
// 		// 	this.initialize_new_page();
// 		// });
//     }
//     prepare_container() {
// 		let list_sidebar = $(`
// 			<div class="list-sidebar overlay-sidebar hidden-xs hidden-sm">
// 				<div class="desk-sidebar list-unstyled sidebar-menu"></div>
// 			</div>
// 		`).appendTo(this.wrapper.find(".layout-side-section"));
// 		this.sidebar = list_sidebar.find(".desk-sidebar");
// 		this.body = this.wrapper.find(".layout-main-section");
// 	}
// }
