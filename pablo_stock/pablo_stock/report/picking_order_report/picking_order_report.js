// Copyright (c) 2025, Frank and contributors
// For license information, please see license.txt

frappe.query_reports["Picking Order Report"] = {
	"filters": [
  {
            "fieldname": "order_number",
            "label": __("Order Number"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "reqd": 0
        }
	]
};
