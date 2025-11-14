# Copyright (c) 2025, Frank and contributors
# For license information, please see license.txt
import frappe
<<<<<<< HEAD
from frappe.model.document import Document
from frappe.permissions import get_doctype_roles
from pablo_stock.pablo_stock import utils
=======
from frappe.model.document import Document , _
>>>>>>> 45c7838 (delivery item)


class PickingOrder(Document):
	def before_insert(self):
		if self.is_new():
			self.status = "Pending"

	@frappe.whitelist()
	def status_in_process(self):
		self.status = "In Process"
		self.save()

	@frappe.whitelist()
	def status_complete(self):
		self.status = "Completed"
		self.save()

	@frappe.whitelist()
	def status_dispatched(self):
		if not self.delivery_item :
			frappe.throw(_("Delivery Item is required."))
		if not self.carrier :
			frappe.throw(_("Carrier is required."))
		if not self.tracking_number :
			frappe.throw(_("Tracking Number is required."))
		self.status = "Dispatched"
<<<<<<< HEAD
		self.save()


def has_permission(doc, user=None, permission_type=None):
	if not user:
		user = frappe.session.user
	if user == "Administrator":
		return True

	workshop = frappe.db.get_value("User", {"name": user}, "custom_workshop")
	roles = frappe.get_roles(user)
	allowed_roles = [
		role
		for role in get_doctype_roles("Picking Order")
		if role not in utils.ROLES_ALLOWED
	]

	if any(role in roles for role in allowed_roles):
		return True

	if doc.workshop == workshop:
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
		for role in get_doctype_roles("Picking Order")
		if role not in utils.ROLES_ALLOWED
	]

	if any(role in roles for role in allowed_roles):
		return None

	if workshop:
		return f"`tabPicking Order`.`workshop` = '{workshop}'"

	return None
=======
		self.save()	

	
>>>>>>> 45c7838 (delivery item)
