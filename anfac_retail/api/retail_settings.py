import frappe
from erpnext.stock.get_item_details import get_pos_profile
from erpnext.stock.doctype.item.item import Item

class CustomItem(Item):
    def add_default_uom_in_conversion_factor_table(self):
        if not self.is_new() and self.has_value_changed("stock_uom"):
            self.uoms = []
            frappe.msgprint(
                 ("Succesfully changed Stock UOM, please redefine conversion factors for new UOM."),
                 alert=True
                 )
        uoms_list = [d.uom for d in self.get("uoms")]
        if self.stock_uom not in uoms_list:
            self.append("uoms", {"uom": self.stock_uom, "conversion_factor": 1})
        if "Pieces" not in uoms_list and self.pieces:
            self.append("uoms", {"uom": "pieces", "conversion_factor": 1})

@frappe.whitelist()
def purchase_invoice_retail(doc , method = None):
    retail_setup = frappe.get_doc("Retail Settings", "Retail Settings")
    if retail_setup.allow_retail:

        if doc.items:
            for item in doc.items:
                item_doc = frappe.get_doc("Item" , item.item_code)
                if item.pieces and item_doc.pieces:
                    
                    item_doc.uoms[1].conversion_factor = 1/float(item.pieces)
                    item_doc.uoms[1].no_of_pieces = float(item.pieces)
                    item_doc.save()  


@frappe.whitelist()
def stock_reconciliation_retail(doc, method = None):
    retail_setup = frappe.get_doc("Retail Settings", "Retail Settings")
    if retail_setup.allow_retail:
        if doc.items:
            for item in doc.items:
                # item_gr = frappe.db.get_value("Item" , item.item_code , "item_group")
                item_doc = frappe.get_doc("Item" , item.item_code)
                if item.pieces   and item_doc.pieces:
                    item_doc.uoms[1].conversion_factor = 1/float(item.pieces)
                    item_doc.uoms[1].no_of_pieces = float(item.pieces)
                    item_doc.save()
                # if not item.pieces and item.item_group == "pieces":
                #     new_doc = frappe.get_doc({
                #         "doctype" : "Mising pieces Items",
                #         "item" : item.item_code,
                #         "qty" :  item.qty,
                #         "pieces" : item.pieces
                #     })
                #     new_doc.save() 

# @frappe.whitelist()
# def sales_invoice_retail(doc, method = None):
#     retail_setup = frappe.get_doc("Retail Setup", "Retail Setup")
#     if retail_setup.pieces:

#         if doc.items:
#              for item in doc.items:
#                 if item.rate <= 0:
#                     frappe.throw(f"Rate can not be zero for <h6>{item.item_code}<h6/>")



# @frappe.whitelist()
# def stock_entry_retail(doc, method = None):
#     retail_setup = frappe.get_doc("Retail Setup", "Retail Setup")
#     if retail_setup.pieces:
#         if doc.items:
#             for item in doc.items:
#                 if item.pieces and item.pieces:
#                     item_doc = frappe.get_doc("Item" , item.item_code)
                    
#                     item_doc.uoms[1].conversion_factor = 1/float(item.pieces)
#                     item_doc.uoms[1].no_of_pieces = float(item.pieces)
#                     item_doc.save()
#                 if not item.pieces and item.item_group == "pieces":
#                     new_doc = frappe.get_doc({
#                     "doctype" : "Mising pieces Items",
#                     "item" : item.item_code,
#                     "qty" :  item.qty,
#                     "pieces" : item.pieces
#                     })
#                     new_doc.save()


@frappe.whitelist()
def item_balance(item_code):
    pos_profile = get_pos_profile( frappe.defaults.get_user_default("company"))
    warehouse = frappe.db.get_value('POS Profile', pos_profile.name,  'warehouse')
    actual_qty=frappe.db.get_value("Bin" , {'warehouse' : warehouse , 'item_code' : item_code} , 'actual_qty')
    return actual_qty



