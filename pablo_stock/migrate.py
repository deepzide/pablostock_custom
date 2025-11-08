import csv
import openpyxl

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
def add_brands():
    file_path = frappe.get_app_path("pablo_stock", "nomenclators", "items.xlsx")
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell for cell in next(sheet.iter_rows(values_only=True))]
    headers_dict = {header: index for index, header in enumerate(headers)}
    for row in sheet.iter_rows(values_only=True, min_row=2):
        brand = row[headers_dict.get("Meta: marca")]
        if not brand:
            continue
        brand = str(brand).strip()
        if not brand:
         continue
        if frappe.db.exists("Brand", brand):
            continue
        brand = frappe.get_doc({
            "doctype": "Brand",
            "brand": brand,
        })
        brand.insert()     
def add_item_group():
    file_path = frappe.get_app_path("pablo_stock", "nomenclators", "items.xlsx")
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell for cell in next(sheet.iter_rows(values_only=True))]
    headers_dict = {header: index for index, header in enumerate(headers)}
    for row in sheet.iter_rows(values_only=True, min_row=2):
        item_group_name = row[headers_dict.get("Categorías")]
        if not item_group_name:
            continue
        item_group_name = str(item_group_name ).strip()
        if frappe.db.exists("Item Group", item_group_name):
            continue
        item_group = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": item_group_name,
        })
        item_group.insert()          
def add_items():
    file_path = frappe.get_app_path("pablo_stock", "nomenclators", "items.xlsx")
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell for cell in next(sheet.iter_rows(values_only=True))]
    headers_dict = {header: index for index, header in enumerate(headers)}
    for row in sheet.iter_rows(values_only=True, min_row=2):
        sku = row[headers_dict.get("SKU")]
        if not sku:
            continue
        item_code = str(sku).strip()
        if frappe.db.exists("Item", item_code):
            continue
        nombre = row[headers_dict.get("Nombre")]
        descripcion = row[headers_dict.get("Descripción")]
        categoria = row[headers_dict.get("Categorías")]
        modelo = row[headers_dict.get("Meta: modelo")]
        origen = row[headers_dict.get("Meta: origen")]
        aplica = row[headers_dict.get("Meta: aplica")]
        #deposito = row[headers_dict.get("Meta: deposito")]
        precio_normal = row[headers_dict.get("Precio normal")] or 0
        precio_rebajado = row[headers_dict.get("Precio rebajado")] or 0
        publicado = row[headers_dict.get("Publicado")]
        marca = None
        if "Meta: marca" in headers_dict:
            marca = row[headers_dict.get("Meta: marca")]
        disabled = 0
        brand_doc = ""
        if marca:
            marca = str(marca).strip()
            if frappe.db.exists("Brand", marca):
                brand_doc = marca 
        if publicado and str(publicado).strip().lower() in ["no", "false", "0"]:
            disabled = 1
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": nombre,
            "description": descripcion,
            "standard_rate": precio_normal,
            "item_group": categoria,      
            "disabled": disabled,            
            "is_stock_item": 1,             
            "is_sales_item": 1,
            "is_purchase_item": 1,
            "custom_origin": origen,
            "custom_item_model": modelo,
            "custom_applies": aplica,
            "custom_discounted_pr": precio_rebajado,
            #"custom_warehouse": deposito,
            "brand": brand_doc,
        })
        item.insert()
def after_migrate():
    add_companys()
    add_brands()
    add_item_group()
    add_items()