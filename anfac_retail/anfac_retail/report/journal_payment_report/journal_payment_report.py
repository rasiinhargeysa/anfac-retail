# Copyright (c) 2022, Anfac Tech and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	_from  = filters.get('from_date')
	to = filters.get('to') 
	
	columns = get_columns()
	data = []

	data = frappe.db.sql(f""" 
	select 
	p.name ,
	p.posting_date,
	p.voucher_no,
	c.account ,
	c.party, 
	c.credit, 
	c.debit
	
	 from 
	 `tabJournal Entry Account`c 
	 left join `tabJournal Entry` p 
	 on p.name = c.parent
	 where p.posting_date between "{_from}" and "{to}" and docstatus !=2 ;
	""")
	return columns, data
def get_columns():
	return [
		"voucher:Link/Journal Entry:120",
		"Posting Date:Date:120",
		"Voucher no:120",
		"Account: Data:220",
		"Party:Data:220",
		"Credit:Currency:120",
		"Debit:Currency:120"
		
		 
		
	
		
	]
