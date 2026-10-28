import frappe
@frappe.whitelist()
def packing_bin_update(doc , method = None):
     if doc.stock_entry_type == "Material Transfer":
          if doc.items:
                for i in doc.items:
                    name = frappe.db.get_value("Packing Bin", {"item_code": i.item_code,"ctn": i.ctn,"ltn": i.ltn,"order_id":i.order_id}, "name")
                    if name:
                        doc_data = frappe.get_doc("Packing Bin" , name)
                        if doc_data:
                            doc_data.actual_qty -= i.qty
                            doc_data.save()
                

