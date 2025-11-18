import csv
import openpyxl

import os
import json
import frappe


def add_companys():
	with open(
		frappe.get_app_path("pablo_stock", "nomenclators", "company.csv")
	) as data:
		companys = list(csv.reader(data, delimiter=","))

		for company in companys:
			if not frappe.db.exists("Company", company[0]) and not frappe.db.exists("Company", {"abbr": company[1].upper()}):
				doc = frappe.get_doc(
					{
						"doctype": "Company",
						"company_name": company[0].upper(),
						"abbr": company[1].upper(),
						"default_currency": company[2].upper(),
						"domain": "Pablo Stock",
						"country": "Uruguay"
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

		


def grant_permissions(role, items):
	for d in items:
		doc = frappe.new_doc("DocPerm")
		doc.role = role
		doc.parenttype = "DocType"
		doc.parentfield = "permissions"
		doc.update(d)


def copy_permissions(doctype):
	for d in frappe.get_all("DocPerm", {"parent": doctype}, "*"):
		if not frappe.db.exists(
			"Custom DocPerm",
			{"parent": d["parent"], "role": d["role"], "permlevel": d["permlevel"]},
		):
			doc = frappe.new_doc("Custom DocPerm")
			doc.update(d)
			doc.insert(ignore_permissions=True)


def grant_custom_permissions(role, items):
	for d in items:
		doc = frappe.new_doc("Custom DocPerm")
		doc.role = role
		doc.update(d)
		doc.insert(ignore_permissions=True)
		copy_permissions(d["parent"])


def has(role, items):
	for i in items:
		if i["parenttype"] == "Report":
			frappe.db.delete(
				"Has Role", {"role": role, "parenttype": "Report", "parent": i["parent"]}
			)
			doc = frappe.new_doc("Has Role")
			doc.role = role
			doc.parentfield = "roles"
			doc.update(i)
			doc.insert(ignore_permissions=True)


def create_role(role):
	if frappe.db.exists("Role", role["name"]):
		doc = frappe.get_doc("Role", role["name"])
		doc.update(role)
		doc.save(ignore_permissions=True)
		frappe.db.delete("DocPerm", {"role": role["name"]})
		frappe.db.delete("Custom DocPerm", {"role": role["name"]})
	else:
		role["doctype"] = "Role"
		doc = frappe.get_doc(role)
		doc.insert(ignore_permissions=True)

	grant_permissions(role["name"], role["doc_perm"])
	grant_custom_permissions(role["name"], role["custom_doc_perm"])
	has(role["name"], role["has"])


def restore_roles():
	folder = frappe.get_app_path("pablo_stock", "roles")
	files = os.listdir(folder)
	for file_name in files:
		if file_name.endswith(".json"):
			file_name = folder + "/" + file_name
			with open(file_name) as f:
				create_role(json.load(f))


def add_domain():
	if not frappe.db.exists("Domain", {"domain": "Pablo Stock"}):
		domain_doc = frappe.new_doc("Domain")
		domain_doc.domain = "Pablo Stock"
		domain_doc.insert()
	if not frappe.db.exists("Has Domain", {"domain": "Pablo Stock"}):
		domain_doc = frappe.new_doc("Has Domain")
		domain_doc.domain = "Pablo Stock"
		domain_doc.parent = "Domain Settings"
		domain_doc.parenttype = "Domain Settings"
		domain_doc.insert()


def disable_workspaces():
	modules_to_show = ["Pablo Stock", "Stock"]

	workspaces_to_hide = frappe.get_all(
		"Workspace",
		filters={
			"module": ["not in", modules_to_show],
			"is_hidden": 0
		},
		pluck="name"
	)
	if workspaces_to_hide:
		frappe.db.set_value("Workspace", {"name": ["in", workspaces_to_hide]}, "is_hidden", 1)

	workspaces_to_show = frappe.get_all(
		"Workspace",
		filters={
			"module": ["in", modules_to_show],
			"is_hidden": 1
		},
		pluck="name"
	)
	if workspaces_to_show:
		frappe.db.set_value("Workspace", {"name": ["in", workspaces_to_show]}, "is_hidden", 0)

	users_workspace = frappe.get_all(
		"Workspace",
		filters={"title": "Users", "is_hidden": 1},
		pluck="name"
	)
	if users_workspace:
		frappe.db.set_value("Workspace", {"name": ["in", users_workspace]}, "is_hidden", 0)


def after_migrate():
	add_domain()
	restore_roles()
	add_companys()
	add_brands()
	add_item_group()
	add_items()
	disable_workspaces()
	frappe.db.commit()
