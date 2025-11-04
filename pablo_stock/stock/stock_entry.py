import frappe
from frappe import _
from erpnext.stock.stock_ledger import get_stock_balance

def validate_negative_stock(doc, method):
    allowed_types = ["Material Issue", "Material Transfer"]
    if doc.stock_entry_type not in allowed_types:
        return

    for d in doc.items:
        if d.s_warehouse:
            actual_qty = get_stock_balance(d.item_code, d.s_warehouse)
            if actual_qty < d.qty:
                frappe.throw(_("No hay suficiente stock para {0} en almacén {1}. Disponible: {2}, Solicitado: {3}")
                             .format(d.item_code, d.s_warehouse, actual_qty, d.qty))
