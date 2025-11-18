import frappe
from frappe.permissions import get_doctype_roles
from pablo_stock.pablo_stock import utils


def has_permission(doc, user=None, permission_type=None):
	if not user:
		user = frappe.session.user
	if user == "Administrator":
		return True

	workshop = frappe.db.get_value("User", {"name": user}, "custom_workshop")
	roles = frappe.get_roles(user)
	allowed_roles = [
		role
		for role in get_doctype_roles("Stock Entry")
		if role not in utils.ROLES_ALLOWED and role != f'Administrador {workshop}'
	]

	if any(role in roles for role in allowed_roles):
		return True

	if f'Administrador {workshop}' in roles:
		return doc.company == workshop

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
		for role in get_doctype_roles("Stock Entry")
		if role not in utils.ROLES_ALLOWED and role != f'Administrador {workshop}'
	]

	if any(role in roles for role in allowed_roles):
		return None

	if f'Administrador {workshop}' in roles:
		return f"`tabStock Entry`.`company` = '{workshop}'"

	return None
