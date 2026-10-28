import frappe

@frappe.whitelist()
def get_last_doc(doc):
    try:
        # frappe.get_last_doc("Task")
        docs = frappe.get_last_doc(doc)
        return docs.voucher_no
    except:
        return 1

@frappe.whitelist()
def get_last_transaction_date(doc):
    try:
        # frappe.get_last_doc("Task")
        docs = frappe.get_last_doc(doc)
        return docs.transaction_date
    except:
        return 1