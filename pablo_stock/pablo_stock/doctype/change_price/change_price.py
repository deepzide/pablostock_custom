# Copyright (c) 2025, Frank and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ChangePrice(Document):
	def before_insert(self):
		if self.is_new():
			self.status = "In Progress"

	
	def update_price(self):
		if not self.item:
			frappe.throw("No se ha definido un producto.")

		item_doc = frappe.get_doc("Item", self.item)
		

		if self.price_type == "Offer Product":
			
			item_doc.custom_discounted_pr = self.price
			item_doc.custom_offer_start_date = self.start_date
			item_doc.custom_offer_end_date = self.end_date

		elif self.price_type == "Change Price":
			item_doc.valuation_rate = self.price

		else:
			frappe.msgprint("El tipo de precio seleccionado no tiene acción definida.")

		item_doc.save(ignore_permissions=True)

	@frappe.whitelist()
	def status_finished(self):
		self.status = "Finished"
		self.save()
		self.update_price()

		