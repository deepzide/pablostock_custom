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
		for role in get_doctype_roles("Item")
		if role not in utils.ROLES_ALLOWED and role != workshop
	]

	if any(role in roles for role in allowed_roles):
		return False

	if workshop in roles:

		stock_entries = frappe.get_all(
			"Stock Entry Detail",
			filters={"item_code": doc.name},
			pluck="parent"
		)

		if not stock_entries:
			return False

		stocks = frappe.get_all(
			"Stock Entry",
			filters={"name": ["in", stock_entries], "company": workshop},
			pluck="name"
		)

		return True if stocks else False

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
		for role in get_doctype_roles("Item")
		if role not in utils.ROLES_ALLOWED and role != f'Administrador {workshop}'
	]

	if any(role in roles for role in allowed_roles):
		return None

	if f'Administrador {workshop}' in roles:

		stock_entries = frappe.get_all(
			"Stock Entry",
			filters={"company": workshop},
			pluck="name"
		)
		items = frappe.get_all(
			"Stock Entry Detail",
			filters={"parent": ["in", stock_entries]},
			pluck="item_code"
		)
		item_list = "', '".join(items)
		return f"`tabItem`.`name` IN ('{item_list}')"

	return None
