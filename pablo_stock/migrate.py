import csv


import frappe


def add_companys():
    with open(
        frappe.get_app_path("pablo_stock", "nomenclators", "company.csv")
    ) as data:
        companys = list(csv.reader(data, delimiter=","))

        for company in companys:
            if not frappe.db.exists("Company", company[0]):
                doc = frappe.get_doc(
                    {
                        "doctype": "Company",
                        "company_name": company[0].upper(),
                        "abbr": company[1].upper(),
                        "default_currency": company[2].upper(),
                    }
                )
                doc.insert()


def after_migrate():
   
    add_companys()