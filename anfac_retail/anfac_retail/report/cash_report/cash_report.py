# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from email import message
import frappe
from frappe import _
from frappe.utils import getdate
from frappe.utils import add_to_date
def execute(filters=None):
	columns, data = [], []
	_from , to = filters.get("from_date") , filters.get("to_date")
	# chart = get_chart_data()
	report_summary = get_report_summary(_from , to)
	message = []
	chart = []
	return get_columns(), get_data(_from , to) , message , chart, report_summary

def get_data(_from , to):
	# frappe.msgprint(get_cash_credit())
	opening = get_account_balance(_from,to)
	recipt =  get_recieved_payment(_from , to) + get_cash_debited(_from , to)
	sales = get_cash_sales(_from , to)
	cash_in = recipt + sales
	payment = get_pay_payment(_from , to) + get_cash_credit(_from , to)
	purchase = get_cash_purchase(_from , to) 
	cash_out = payment + purchase
	closing = opening + cash_in - cash_out

	return [{
		'report_date' : to, 
		'opening' :opening,
		"cash_in" : "<p class = 'primary'>  </p>",
		"sales" : sales,
		"reciept" :  recipt,
		"cash_out" : "<p class = 'primary'>  </p>",
		"payment" : payment,
		"purchase" : purchase,
		"closing" : closing
		
		 }]


def get_columns():
	columns = [
		{
			"label": _("Date"),
			"fieldtype": "Date",
			"fieldname": "report_date",
			
			"width": 100,
		},
		{
			"label": _("Opening"),
			"fieldtype": "Currency",
			"fieldname": "opening",
			
			"width": 100,
		},
		{
			"label": _(""),
			"fieldtype": "Data",
			"fieldname": "cash_in",
			
			"width": 100,
		},
			{
			"label": _("Sales"),
			"fieldtype": "Currency",
			"fieldname": "sales",
			
			"width": 100,
		},
			{
			"label": _("Reciept"),
			"fieldtype": "Currency",
			"fieldname": "reciept",
			
			"width": 100,
		},
		
		{
			"label": _(""),
			"fieldtype": "Data",
			"fieldname": "cash_out",
			
			"width": 100,
		},
			{
			"label": _("Payment"),
			"fieldtype": "Currency",
			"fieldname": "payment",
			
			"width": 100,
		},
			{
			"label": _("Purchase"),
			"fieldtype": "Currency",
			"fieldname": "purchase",
			
			"width": 100,
		},

		{
			"label": _("Closing"),
			"fieldtype": "Currency",
			"fieldname": "closing",
			
			"width": 150,
		},
	]

	return columns


# Get Opening Balance
def get_account_balance(_from ,to):
	# pre =adddate(getdate(_from) , datys = -1 ) 
	pre = add_to_date(_from, days=-1, as_string=True)
	report_bl = frappe.get_doc("Report", "Account Balance")
	report_filters = {"report_date":pre, "account_type" :"Cash"}

	columns, data = report_bl.get_data(
           limit=500, user="Administrator", filters=report_filters, as_dict=True
    )

	

	return data[0]['balance']

#in cass
#Get Cash Sales
def get_cash_sales(_from , to):

	sales = frappe.db.sql(f""" 
    select sum(paid_amount) as amount
	 from `tabSales Invoice`
      where is_pos = 1 and paid_amount > 0 
	  and posting_date between "{_from}" and "{to}"
	  and docstatus !=2
     """, as_dict = 1)
	return sales[0]['amount']  if sales[0]['amount'] else 0


#Get Payment Entry (Recieve)

def get_recieved_payment(_from , to):
	pv = frappe.db.sql(f"""
    
	select sum(paid_amount) as amount 
	from `tabPayment Entry` 
    where payment_type = "Receive" 
	and posting_date between "{_from}" and "{to}"
	and docstatus !=2
    
    ;
    """, as_dict =1
    )

	return pv[0]['amount'] if pv[0]['amount'] else 0

# Get Cash Debited in Journal Entry

def get_cash_debited(_from , to):
	cash_debit = frappe.db.sql(f""" 
	 select sum(c.debit) as amount
	 from `tabJournal Entry Account` c 
	 left join `tabJournal Entry` p 
	 on c.parent = p.name 
	 where c.account_type =  'Cash'  
	 and p.posting_date between "{_from}" and "{to}"  
	 and p.docstatus !=2
	 """ , as_dict = 1)
	return cash_debit[0]['amount'] if cash_debit[0]['amount'] else 0


#Get purchase return

def get_purchase_return(_from , to):
	purchase = frappe.db.sql(f""" 
    select sum(grand_total) as amount  
	from `tabPurchase Invoice`       
	where is_paid = 1 
	and is_return = 1    
	and posting_date between "{_from}" and "{to}"
	and docstatus !=2
     """, as_dict = 1)
	return purchase[0]['amount'] if purchase[0]['amount'] else 0




#out cash
#Get Cash Purchase
def get_cash_purchase(_from , to):
	purchase = frappe.db.sql(f""" 
    select sum(grand_total) as amount  
	from `tabPurchase Invoice`       
	where is_paid = 1     
	and posting_date between "{_from}" and "{to}"
	and docstatus !=2
     """, as_dict = 1)
	return purchase[0]['amount'] if purchase[0]['amount'] else 0


#Get Payment Entry (Pay)

def get_pay_payment(_from , to):
	pv = frappe.db.sql(f"""
    
	select sum(paid_amount) as amount 
	from `tabPayment Entry` 
    where payment_type = "Pay" 
	and posting_date between "{_from}" and "{to}"
    and docstatus !=2
    ;
    """, as_dict =1
    )

	return pv[0]['amount'] if pv[0]['amount'] else 0


# Get Cash Credit in Journal Entry

def get_cash_credit(_from , to):
	cash_credit = frappe.db.sql(f""" 
	 select sum(c.credit) as amount
	 from `tabJournal Entry Account` c 
	 left join `tabJournal Entry` p 
	 on c.parent = p.name 
	 where c.account_type =  'Cash'  
	 and posting_date between "{_from}" and "{to}"  
	 and p.docstatus !=2
	 """ , as_dict = 1)
	return cash_credit[0]['amount'] if cash_credit[0]['amount'] else 0


#Get sales return

def get_sales_return(_from , to):
	sales = frappe.db.sql(f""" 
    select sum(paid_amount) as amount
	 from `tabSales Invoice`
      where is_pos = 1
	  and is_return = 1
	   and paid_amount > 0 
	  and posting_date between "{_from}" and "{to}"
	  and docstatus !=2
     """, as_dict = 1)
	return sales[0]['amount'] if sales[0]['amount'] else 0




def get_report_summary(_from , to):
	opening = get_account_balance(_from, to)
	recipt =  get_recieved_payment(_from , to) + get_cash_debited(_from , to)
	sales = get_cash_sales(_from , to)
	cash_in = recipt + sales
	payment = get_pay_payment(_from , to) + get_cash_credit(_from , to)
	purchase = get_cash_purchase(_from , to) 
	cash_out = payment + purchase
	closing = opening + cash_in - cash_out
	currency =  frappe.get_cached_value(
		"Company", frappe.defaults.get_global_default("company"), "default_currency"
	)
	return [
		{
			"value": opening,
			"label": "Opeing",
			 "datatype": "Currency", 
			 "currency": currency
		},
		{
			"value": cash_in,
			"label": "Cash In",
			"datatype": "Currency",
			"currency": currency,
		},
		{
			"value": cash_out, 
			"label": "Cash Out",
			 "datatype": "Currency", 
			 "currency": currency},
		{
			"value": closing,
			"label": "Closing",
			"indicator": "Green" if closing > 0 else "Red",
			"datatype": "Currency",
			"currency": currency,
		},
	]



# def get_chart_data(filters, columns, asset, liability, equity):
# 	labels = [d.get("label") for d in columns[2:]]

# 	asset_data, liability_data, equity_data = [], [], []

# 	for p in columns[2:]:
# 		if asset:
# 			asset_data.append(asset[-2].get(p.get("fieldname")))
# 		if liability:
# 			liability_data.append(liability[-2].get(p.get("fieldname")))
# 		if equity:
# 			equity_data.append(equity[-2].get(p.get("fieldname")))

# 	datasets = []
# 	if asset_data:
# 		datasets.append({"name": _("Assets"), "values": asset_data})
# 	if liability_data:
# 		datasets.append({"name": _("Liabilities"), "values": liability_data})
# 	if equity_data:
# 		datasets.append({"name": _("Equity"), "values": equity_data})

# 	chart = {"data": {"labels": labels, "datasets": datasets}}

# 	if not filters.accumulated_values:
# 		chart["type"] = "bar"
# 	else:
# 		chart["type"] = "line"

# 	return chart
