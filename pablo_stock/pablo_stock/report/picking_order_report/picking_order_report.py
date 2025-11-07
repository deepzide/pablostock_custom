# Copyright (c) 2025, Frank and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = [
        {"label": "Order Number", "fieldname": "order_number", "fieldtype": "Link", "options": "Sales Order", "width": 180},
        {"label": "Workshop", "fieldname": "workshop", "fieldtype": "Data", "width": 250},
        {"label": "Ubications", "fieldname": "ubications", "fieldtype": "Data", "width": 250},
        {"label": "Pieces", "fieldname": "pieces", "fieldtype": "Data", "width": 250},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Int", "width": 250},
        {"label": "Origin", "fieldname": "origin", "fieldtype": "Data", "width": 250},
    ]

    conditions = ""
    if filters.get("order_number"):
        conditions += " and order_number = %(order_number)s"

    data = frappe.db.sql(f"""
        SELECT
            order_number,
            workshop,
            ubications,
            pieces,
            amount,
            origin
        FROM
            `tabPicking Order`
        WHERE
            1=1 {conditions}
        ORDER BY modified DESC
    """, filters, as_dict=1)

    return columns, data
