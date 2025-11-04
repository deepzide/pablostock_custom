// Copyright (c) 2025, Frank and contributors
// For license information, please see license.txt

function set_filter_based_on() {
  let based_on = frappe.query_report.get_filter_value("filter_based_on");
  frappe.query_report.toggle_filter_display("day", based_on === "Date Range");
  frappe.query_report.toggle_filter_display("from_date", based_on === "Day");
  frappe.query_report.toggle_filter_display("to_date", based_on === "Day");

  if (based_on === "Date Range") {
    frappe.query_report.set_filter_value({ day: null });
    let from_date = frappe.query_report.get_filter_value("from_date");
    let to_date = frappe.query_report.get_filter_value("to_date");
    if (from_date && to_date) {
      frappe.query_report.set_filter_value("posting_date", [from_date, to_date]);
    }
  } else if (based_on === "Day") {
    let selected_day = frappe.query_report.get_filter_value("day") || moment().format("YYYY-MM-DD");
    frappe.query_report.set_filter_value("posting_date", [selected_day, selected_day]);
  }

  frappe.query_report.refresh();
}

frappe.query_reports["Daily Stock Entry Movements"] = {
  "filters": [
    {
      "fieldname": "filter_based_on",
      "label": __("Filter Based On"),
      "fieldtype": "Select",
      "options": ["Day", "Date Range"],
      "reqd": 1,
      "default": "Day",
      on_change: set_filter_based_on,
    },
    {
      "fieldname": "day",
      "label": __("Day"),
      "fieldtype": "Date",
      "default": moment().format("YYYY-MM-DD"),
      on_change: () => {
        let selected_day = frappe.query_report.get_filter_value("day");
        if (selected_day) {
          frappe.query_report.set_filter_value("posting_date", [selected_day, selected_day]);
          frappe.query_report.refresh();
        }
      }
    },
    {
      "fieldname": "from_date",
      "label": __("From Date"),
      "fieldtype": "Date",
      "on_change": () => {
        let from_date = frappe.query_report.get_filter_value("from_date");
        let to_date = frappe.query_report.get_filter_value("to_date");
        if (from_date && to_date) {
          frappe.query_report.set_filter_value("posting_date", [from_date, to_date]);
          frappe.query_report.refresh();
        }
      },
      "hidden": 1
    },
    {
      "fieldname": "to_date",
      "label": __("To Date"),
      "fieldtype": "Date",
      "on_change": () => {
        let from_date = frappe.query_report.get_filter_value("from_date");
        let to_date = frappe.query_report.get_filter_value("to_date");
        if (from_date && to_date) {
          frappe.query_report.set_filter_value("posting_date", [from_date, to_date]);
          frappe.query_report.refresh();
        }
      },
      "hidden": 1
    },
    {
      "fieldname": "posting_date",
      "label": __("Posting Date"),
      "fieldtype": "DateRange",
      "reqd": 1,
      "hidden": 1
    },
    {
      "fieldname": "item_code",
      "label": __("Item"),
      "fieldtype": "Link",
      "options": "Item",
    },
    {
      "fieldname": "warehouse",
      "label": __("Warehouse"),
      "fieldtype": "Link",
      "options": "Warehouse",
    },
    {
      "fieldname": "stock_entry_type",
      "label": __("Stock Entry Type"),
      "fieldtype": "Select",
      "options": "\nMaterial Receipt\nMaterial Issue\nMaterial Transfer\nRepack\nManufacture",
    },
  ],

  onload: function () {
    set_filter_based_on();
  }
};
