// Copyright (c) 2025, Frank and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Stock Entry Movements"] = {
    "filters": [
          {
            "fieldname": "posting_date",
            "label": __("Posting Date"),
            "fieldtype": "DateRange",
            "reqd": 1,
        },
        {
            "fieldname": "item_code",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "reqd": 0
        },
        {
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "reqd": 0
        },
        {
            "fieldname": "stock_entry_type",
            "label": __("Stock Entry Type"),
            "fieldtype": "Select",
            "options": "\nMaterial Receipt\nMaterial Issue\nMaterial Transfer\nRepack\nManufacture",
            "reqd": 0
        }
    ]
};
