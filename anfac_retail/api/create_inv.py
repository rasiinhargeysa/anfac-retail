import frappe
from erpnext.stock.get_item_details import get_pos_profile
@frappe.whitelist()
def create_inv(doc_name ,dt , is_sales_return = False ,  is_credit = False):
    pos_profile = get_pos_profile( frappe.defaults.get_user_default("company"))
    mode_of_payment = frappe.db.get_value('POS Payment Method', {"parent": pos_profile.name},  'mode_of_payment')
    default_account = frappe.db.get_value('Mode of Payment Account', {"parent": mode_of_payment},  'default_account')
    cost_center = frappe.db.get_value('POS Profile', pos_profile.name,  'write_off_cost_center')
    warehouse = ""
    cash_sales = frappe.get_doc(dt , doc_name)
    warehouse = cash_sales.set_warehouse
    customer = cash_sales.customer
    # frappe.msgprint(order_doc.name)
    items = []
    empty_items = ""
    for item in cash_sales.items:
        # item_qty = frappe.db.get_value("Batch" , {"item" :item.item_code  }, "batch_qty" )
        # if float(item_qty) <= 0 :
        #     empty_items += item.item_code + ' , '
        # #     frappe.throw(
        # #     title='Ogerysiis',
            
        # #     exc=FileNotFoundError
        # # )
        qty = item.qty
        if not cash_sales.set_warehouse:
           warehouse = frappe.db.get_value('POS Profile', pos_profile.name,  'warehouse')
        if is_sales_return:
            qty = float(item.qty) * (-1)
        items.append({
            "item_code" : item.item_code,
            "rate" : item.rate,
            "qty" : qty,
            "warehouse": warehouse,
        })
    payments = []
    # is_pos = 0
    # if not is_credit:
    # b =frappe.defaults.get_user_permissions(frappe.session.user)
    # pos =b['POS Profile'][0].doc
    # pos = frappe.get_doc("POS Profile" , pos)
    # payment = pos.payments
    
    paid_amount = cash_sales.grand_total
    is_pos = 0
    pos_profile_name = ''
    account = ''
    if is_sales_return and cash_sales.refund == 1:
        is_pos = 1
        if cash_sales.pos_profile:
            pos_profile_name = cash_sales.pos_profile
        paid_amount = cash_sales.grand_total * (-1)
        payments.append(
                {
                    "mode_of_payment" : mode_of_payment,
                    "amount" : paid_amount
                    
                }
            )
        
        
 
        
    
    
    if not is_credit and not is_sales_return :
        is_pos = 1
        if cash_sales.pos_profile:
            pos_profile_name = cash_sales.pos_profile
        payments.append(
                {
                    "mode_of_payment" : mode_of_payment,
                    "amount" : paid_amount
                    
                }
            )

    # if is_sales_return:
    #     paid_amount = cash_sales.grand_total * (-1)
    # is_pos = 0
    # if  is_refund:
    #     is_pos = 1
    #     payments.append(
    #             {
    #                 "mode_of_payment" : "Cash",
    #                 "amount" : paid_amount
                    
    #             }
    #         )

    is_return = 0
    if is_sales_return :
         is_return = 1 
    sales_doc = frappe.get_doc({
        "doctype" : "Sales Invoice",
        "is_return" : is_return,
        "posting_date" : cash_sales.transaction_date,
        "customer": customer,
       "is_pos" : is_pos,
        "cost_center":cost_center,
        "set_warehouse" : warehouse,
        "write_off_cost_center":cost_center,
        "loyalty_redemption_cost_center": cost_center,
        "discount_amount" : cash_sales.discount_amount,
        "payments": payments,
        "voucher_no" : cash_sales.name,
        "pos_profile":pos_profile_name,
        "items" : items,
       
    })
   
    sales_doc.insert()
    sales_doc.submit()
    frappe.msgprint('Billed successfully')
    return sales_doc
    # cash_sales.sales_invoice = sales_doc.name
    # cash_sales.save()
    
    




def purchase(doc_name ,dt , is_purchase_return = False , is_credit = False):
    pos_profile = get_pos_profile( frappe.defaults.get_user_default("company"))
    mode_of_payment = frappe.db.get_value('POS Payment Method', {"parent": pos_profile.name},  'mode_of_payment')
    default_account = frappe.db.get_value('Mode of Payment Account', {"parent": mode_of_payment},  'default_account')
    cost_center = frappe.db.get_value('POS Profile', pos_profile.name,  'write_off_cost_center')
    cash_sales = frappe.get_doc(dt , doc_name)
    supplier = cash_sales.supplier
    # frappe.msgprint(order_doc.name)
    items = []
    empty_items = ""
    for item in cash_sales.items:
        # item_qty = frappe.db.get_value("Batch" , {"item" :item.item_code  }, "batch_qty" )
        # if float(item_qty) <= 0 :
        #     empty_items += item.item_code + ' , '
        # #     frappe.throw(
        # #     title='Ogerysiis',
            
        # #     exc=FileNotFoundError
        # # )
        qty = item.qty
        if is_purchase_return:
            qty = float(item.qty) * (-1)
        items.append({
            "item_code" : item.item_code,
            "rate" : item.rate,
            "qty" : qty
        })
    payments = []
    
    paid_amount = cash_sales.rounded_total
    is_paid = 0
    account = ''
    if is_purchase_return and cash_sales.refund == 1:
        is_paid = 1
        account = cash_sales.account
        paid_amount = cash_sales.grand_total * (-1)
        
 
        
    
    
    if not is_credit and not is_purchase_return :
        is_paid = 1
        account = cash_sales.account
        
                    
        
                    
          
    is_return = 0
    if is_purchase_return :
         is_return = 1 
    frappe.msgprint(str(cash_sales.date))
    pur_doc = frappe.get_doc({
        "doctype" : "Purchase Invoice",
        "posting_date" : cash_sales.date,
        "is_return" : is_return,
        "supplier": supplier,
        "discount_amount" : cash_sales.discount_amount,
        "is_paid" : is_paid,
        "discount_amount" : cash_sales.discount_amount,
        "cash_bank_account" : default_account,
        "paid_amount" : paid_amount,
        "bill_no" : cash_sales.supplier_invoice,
        # "payments": payments,
        "voucher_no" : cash_sales.supplier_invoice,
       "set_warehouse": cash_sales.set_warehouse,
        "items" : items,
       
    })
   
    pur_doc.save()
    pur_doc.submit()
    frappe.msgprint('Billed successfully')
    return pur_doc
    # cash_sales.sales_invoice = sales_doc.name
    # cash_sales.save()
    
    
