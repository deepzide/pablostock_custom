# Copyright (c) 2025, Frank and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document


class PickingOrder(Document):
	def before_insert(self):
		if self.is_new():
			self.db_set("status", "Pending")
