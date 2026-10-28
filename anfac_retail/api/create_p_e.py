import frappe
@frappe.whitelist()
def payment(doc_name ,dt):
    pay = frappe.get_doc(dt , doc_name)
    references = []
    if pay.references:
        for i in pay.references:
            references.append({"reference_doctype": i.reference_doctype, "reference_name": i.reference_name, "total_amount": i.total_amount, "outstanding_amount": i.outstanding_amount, "allocated_amount": i.allocated_amount})
    
    payment_entry = frappe.get_doc({
        "doctype" : "Payment Entry",
        "payment_type" : pay.payment_type,
        "posting_date" : pay.posting_date,
        "company" : pay.company,
        "party_type": pay.party_type,
        "party" : pay.party,
        "paid_from" : pay.paid_from,
        "paid_to": pay.paid_to,
        "received_amount": pay.received_amount,
        "paid_amount": pay.paid_amount,
        "voucher_no" : pay.voucher_no,
        "references" : references,
       
    })
   
    payment_entry.save()
    payment_entry.submit()
    frappe.msgprint('Billed successfully')
    return payment_entry
    # cash_sales.sales_invoice = sales_doc.name
    # cash_sales.save()
    
    
