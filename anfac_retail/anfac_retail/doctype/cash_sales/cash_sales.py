# Copyright (c) 2022, Anfac Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from anfac_retail.api.create_inv import create_inv
from frappe.model.document import Document

class CashSales(Document):
	
	def on_submit(self):
		# make_property_setter('Cash Sales', "transaction_date", "default", self.transaction_date, "Date")
		# frappe.msgprint("ok")
		sales_doc = create_inv(self.name , dt = 'Cash Sales')
		self.sales_invoice = sales_doc.name
		self.save()
	def on_cancel(self):
		if self.sales_invoice:
			

			sales_doc = frappe.get_doc("Sales Invoice" , self.sales_invoice)
			sales_doc.cancel()


