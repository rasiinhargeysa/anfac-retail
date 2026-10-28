# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import frappe
from anfac_retail.api.create_inv import purchase
from frappe.model.document import Document


class CashPurchase(Document):
	def on_submit(self):
		# frappe.msgprint("ok")
		purchase_doc = purchase(self.name ,dt = 'Cash Purchase')
		self.purchase_invoice = purchase_doc.name
		self.save()
	def on_cancel(self):
		if self.purchase_invoice:
			purchase_doc = frappe.get_doc("Purchase Invoice" , self.purchase_invoice)
			purchase_doc.cancel()
