frappe.ui.form.on("User", {
	refresh(frm) {
		if (frm.is_new()) {
			frappe.call({
				method: "pablo_stock.overrides.user.get_user_workshop",
				callback: function (r) {
					frm.doc.custom_workshop = r.message;
					frm.refresh_field("custom_workshop");
				}
			});
		}
	}
});
