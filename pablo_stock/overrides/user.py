import frappe
from frappe import _
from frappe.core.doctype.user.user import User
from frappe.permissions import get_doctype_roles
from pablo_stock.pablo_stock import utils


class CustomUser(User):
	def before_save(self):
		if self.is_new() and not self.custom_workshop:
			custom_workshop = get_user_workshop()
			self.custom_workshop = custom_workshop

	def after_insert(self):
		super().after_insert()

		user = frappe.session.user
		roles = frappe.get_roles(user)
		custom_workshop = self.custom_workshop or frappe.db.get_value(
			"User", {"name": user}, "custom_workshop")

		if ("Workshop General Manager" in roles and user != "Administrator") or custom_workshop:
			role_name = f"Operario {custom_workshop}"

			if not frappe.db.exists("Has Role", {"parent": self.name, "role": role_name}):
				frappe.get_doc({
					"doctype": "Has Role",
					"parent": self.name,
					"parenttype": "User",
					"parentfield": "roles",
					"role": role_name
				}).insert(ignore_permissions=True)


@frappe.whitelist()
def get_user_workshop():
	user = frappe.session.user
	roles = frappe.get_roles(user)
	if "Workshop General Manager" not in roles:
		custom_workshop = frappe.db.get_value("User", {"name": user}, "custom_workshop")
		if custom_workshop:
			frappe.msgprint(
				_("Users can only be created who belong to the workshop {0}").format(
					custom_workshop),
				indicator="blue",
				alert=True,
				title="Info",
			)
			return custom_workshop
	return None


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

	if doc.custom_workshop == workshop:
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
		for role in get_doctype_roles("User")
		if role not in utils.ROLES_ALLOWED and role != f'Administrador {workshop}'
	]

	if any(role in roles for role in allowed_roles):
		return None

	if workshop:
		return f"`tabUser`.`custom_workshop` = '{workshop}'"

	return None
