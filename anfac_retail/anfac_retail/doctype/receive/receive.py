# Copyright (c) 2022, Anfac Tech and contributors
# For license information, please see license.txt
import frappe
from anfac_retail.api.create_p_e import payment
from frappe.model.document import Document

class Receive(Document):
	def on_submit(self):
		frappe.msgprint("ok")
		payments = payment(self.name,  dt = 'Receive')
		self.payment_entry = payments.name
		self.save()
	def on_cancel(self):
		if self.payment_entry:
			payments = frappe.get_doc("Payment Entry" , self.payment_entry)
			if payments.docstatus == 1:
				payments.cancel()
