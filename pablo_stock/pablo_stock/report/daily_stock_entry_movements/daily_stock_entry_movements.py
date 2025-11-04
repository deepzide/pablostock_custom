# Copyright (c) 2025, Frank and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = [
        {"label": "Fecha", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Hora", "fieldname": "posting_time", "fieldtype": "Time", "width": 80},
        {"label": "Tipo Movimiento", "fieldname": "stock_entry_type", "fieldtype": "Data", "width": 160},
        {"label": "Nº Movimiento", "fieldname": "name", "fieldtype": "Link", "options": "Stock Entry", "width": 160},
        {"label": "Compañía", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 160},
        {"label": "Código de Ítem", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
        {"label": "Producto", "fieldname": "item_name", "fieldtype": "Data", "width": 180},
        {"label": "Grupo", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 120},
        {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 80},
        {"label": "Cantidad", "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": "Bodega Origen", "fieldname": "s_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 160},
        {"label": "Bodega Destino", "fieldname": "t_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 160},
    ]

    conditions = []

    # Filtro Day
    if filters.get("filter_based_on") == "Day" and filters.get("day"):
        conditions.append("se.posting_date = %(day)s")

    # Filtro Date Range
    elif filters.get("filter_based_on") == "Date Range":
        from_date = filters.get("from_date")
        to_date = filters.get("to_date")
        if from_date and to_date:
            conditions.append("se.posting_date BETWEEN %(from_date)s AND %(to_date)s")

    # Otros filtros opcionales
    if filters.get("stock_entry_type"):
        conditions.append("se.stock_entry_type = %(stock_entry_type)s")
    if filters.get("item_code"):
        conditions.append("sed.item_code = %(item_code)s")
    if filters.get("warehouse"):
        conditions.append("(sed.s_warehouse = %(warehouse)s OR sed.t_warehouse = %(warehouse)s)")

    if not conditions:
        return columns, []

    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT
            se.posting_date,
            se.posting_time,
            se.stock_entry_type,
            se.name,
            se.company,
            sed.item_code,
            sed.item_name,
            i.item_group,
            sed.uom,
            sed.qty,
            sed.s_warehouse,
            sed.t_warehouse
        FROM
            `tabStock Entry` se
        INNER JOIN
            `tabStock Entry Detail` sed ON sed.parent = se.name
        LEFT JOIN
            `tabItem` i ON i.name = sed.item_code
        WHERE
            {where_clause}
        ORDER BY
            se.posting_date DESC, se.name DESC
        LIMIT 1000
    """

    data = frappe.db.sql(query, filters, as_dict=True)
    return columns, data
