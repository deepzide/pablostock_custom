import frappe
import json
import os
from frappe import _
from erpnext.setup.doctype.company.company import Company
from pablo_stock.migrate import restore_roles
from frappe.permissions import get_doctype_roles
from pablo_stock.pablo_stock import utils
from frappe.desk.doctype.notification_settings.notification_settings import \
	create_notification_settings


class CustomCompany(Company):
	def after_insert(self):
		try:
			role_name = f'Administrador {self.company_name}'
			role_name_lower = role_name.lower().replace(' ', '_')
			role_email = f"{role_name_lower}@gmail.com"

			role_name_operator = f'Operario {self.company_name}'
			role_name_operator_lower = role_name_operator.lower().replace(' ', '_')

			if not frappe.db.exists("Role", role_name):
				create_manager_role(role_name, role_name_lower)
			if not frappe.db.exists("Role", role_name_operator):
				create_operator_role(role_name_operator, role_name_operator_lower)
			restore_roles()

			if not frappe.db.exists("User", role_email):
				create_user(role_name, role_name_lower, role_email, self.company_name)

			frappe.msgprint(
				_("The roles of administrator and workshop operator were created, as well as the user corresponding to the administrator role"),
				indicator="green",
				alert=True,
				title="Success",
			)
		except Exception:
			frappe.db.rollback()

	def after_rename(self, olddn, newdn, merge=False):
		super().after_rename(olddn, newdn, merge=merge)
		olddn_name = f'Administrador {olddn}'
		newdn_name = f'Administrador {newdn}'

		if frappe.db.exists("Role", {"role_name": olddn_name}):
			frappe.rename_doc("Role", olddn_name, newdn_name)

		if frappe.db.exists("User", {"first_name": olddn_name}):
			old_name_lower = olddn_name.lower().replace(' ', '-')
			new_name_lower = newdn_name.lower().replace(' ', '-')
			user = frappe.get_doc("User", {"first_name": olddn_name})
			if user.email == f"{old_name_lower}@gmail.com":
				user.email = f"{new_name_lower}@gmail.com"
			if user.user_name == old_name_lower:
				user.user_name = new_name_lower
			user.save(ignore_permissions=True)
			frappe.rename_doc("User", olddn_name, newdn_name)


def create_user(role_name, role_name_lower, role_email, company):
	if not frappe.db.exists("User", role_email):
		frappe.db.sql("""
			INSERT INTO `tabUser`
			(name, email, first_name, username, full_name, enabled, language, custom_workshop, creation, modified, modified_by, owner)
			VALUES (%s, %s, %s, %s, %s, 1, 'es-MX', %s, NOW(), NOW(), %s, %s)
		""", (role_email, role_email, role_name, role_name_lower, role_name, company,
			  frappe.session.user, frappe.session.user))

		create_notification_settings(role_email)
		frappe.cache.delete_key("users_for_mentions")
		frappe.cache.delete_key("enabled_users")

		if not frappe.db.exists("Has Role", {"parent": role_email, "role": role_name}):
			frappe.db.sql("""
				INSERT INTO `tabHas Role`
				(name, parent, parenttype, parentfield, role, creation, modified, modified_by, owner)
				VALUES (%s, %s, 'User', 'roles', %s, NOW(), NOW(), %s, %s)
			""", (role_name, role_email, role_name, frappe.session.user, frappe.session.user))


def create_manager_role(role_name, role_name_lower):
	perm_dict = [
		{
			"parent": "User",
			"permlevel": 0,
			"select": 1,
			"read": 1,
			"write": 1,
			"create": 1,
			"submit": 0,
			"cancel": 0,
			"delete": 0,
			"amend": 0,
			"report": 0,
			"export": 1,
			"import": 0,
			"share": 0,
			"print": 0,
			"email": 1,
			"if_owner": 0,
			"set_user_permissions": 0
		},
		{
			"parent": "Company",
			"permlevel": 0,
			"select": 1,
			"read": 1,
			"write": 1,
			"create": 0,
			"submit": 0,
			"cancel": 0,
			"delete": 0,
			"amend": 0,
			"report": 0,
			"export": 1,
			"import": 0,
			"share": 0,
			"print": 0,
			"email": 1,
			"if_owner": 0,
			"set_user_permissions": 0
		},
		{
			"parent": "Item",
			"permlevel": 0,
			"select": 1,
			"read": 1,
			"write": 1,
			"create": 0,
			"submit": 0,
			"cancel": 0,
			"delete": 0,
			"amend": 0,
			"report": 1,
			"export": 0,
			"import": 0,
			"share": 0,
			"print": 0,
			"email": 0,
			"if_owner": 0,
			"set_user_permissions": 0
		},
		{
			"parent": "Stock Entry",
			"permlevel": 0,
			"select": 1,
			"read": 1,
			"write": 1,
			"create": 1,
			"submit": 0,
			"cancel": 0,
			"delete": 1,
			"amend": 0,
			"report": 1,
			"export": 1,
			"import": 0,
			"share": 0,
			"print": 0,
			"email": 1,
			"if_owner": 0,
			"set_user_permissions": 0
		},
		{
			"parent": "Picking Order",
			"permlevel": 0,
			"select": 1,
			"read": 1,
			"write": 1,
			"create": 1,
			"submit": 0,
			"cancel": 0,
			"delete": 1,
			"amend": 0,
			"report": 1,
			"export": 1,
			"import": 0,
			"share": 0,
			"print": 0,
			"email": 1,
			"if_owner": 0,
			"set_user_permissions": 0
		}
	]

	create_role_json(role_name, perm_dict, role_name_lower)


def create_role_json(role_name, perm_dict, role_name_lower):
	role_data = {
		"name": role_name,
		"role_name": role_name,
		"desk_access": 1,
		"search_bar": 1,
		"notifications": 1,
		"list_sidebar": 1,
		"bulk_actions": 1,
		"view_switcher": 1,
		"form_sidebar": 1,
		"timeline": 1,
		"dashboard": 1,
		"restrict_to_domain": "Pablo Stock",
		"doc_perm": perm_dict,
		"custom_doc_perm": perm_dict,
		"has": []
	}
	base_path = frappe.get_app_path("pablo_stock", "roles")
	os.makedirs(base_path, exist_ok=True)

	file_path = os.path.join(base_path, f"{role_name_lower}.json")

	with open(file_path, "w", encoding="utf-8") as f:
		json.dump(role_data, f, ensure_ascii=False, indent=2)


def create_operator_role(role_name, role_name_lower):
	perm_dict = [
		{
			"parent": "Item",
			"permlevel": 0,
			"select": 1,
			"read": 1,
			"write": 1,
			"create": 0,
			"submit": 0,
			"cancel": 0,
			"delete": 0,
			"amend": 0,
			"report": 1,
			"export": 0,
			"import": 0,
			"share": 0,
			"print": 0,
			"email": 0,
			"if_owner": 0,
			"set_user_permissions": 0
		},
		{
			"parent": "Stock Entry",
			"permlevel": 0,
			"select": 1,
			"read": 1,
			"write": 1,
			"create": 1,
			"submit": 0,
			"cancel": 0,
			"delete": 1,
			"amend": 0,
			"report": 1,
			"export": 1,
			"import": 0,
			"share": 0,
			"print": 0,
			"email": 1,
			"if_owner": 0,
			"set_user_permissions": 0
		},
		{
			"parent": "Picking Order",
			"permlevel": 0,
			"select": 1,
			"read": 1,
			"write": 1,
			"create": 1,
			"submit": 0,
			"cancel": 0,
			"delete": 1,
			"amend": 0,
			"report": 1,
			"export": 1,
			"import": 0,
			"share": 0,
			"print": 0,
			"email": 1,
			"if_owner": 0,
			"set_user_permissions": 0
		}
	]

	create_role_json(role_name, perm_dict, role_name_lower)


def has_permission(doc, user=None, permission_type=None):
	if not user:
		user = frappe.session.user
	if user == "Administrator":
		return True

	workshop = frappe.db.get_value("User", {"name": user}, "custom_workshop")

	roles = frappe.get_roles(user)
	allowed_roles = [
		role
		for role in get_doctype_roles("Company")
		if role not in utils.ROLES_ALLOWED and role != f'Administrador {workshop}'
	]

	if any(role in roles for role in allowed_roles):
		return True

	if doc.company_name == workshop:
		return True

	return False


def get_permission_query_conditions(user=None):
	if not user:
		user = frappe.session.user
	if user == "Administrator":
		return None

	workshop = frappe.db.get_value("User", {"name": user}, "custom_workshop")

	roles = frappe.get_roles(user)
	allowed_roles = [
		role
		for role in get_doctype_roles("Company")
		if role not in utils.ROLES_ALLOWED and role != f'Administrador {workshop}'
	]

	if any(role in roles for role in allowed_roles):
		return None

	if workshop:
		return f"`tabCompany`.`company_name` = '{workshop}'"

	return None
