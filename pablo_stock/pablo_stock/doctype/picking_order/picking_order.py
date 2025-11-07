# Copyright (c) 2025, Frank and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document


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
		self.status = "Dispatched"
		self.save()	
	
