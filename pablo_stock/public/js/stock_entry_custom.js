frappe.ui.form.on("Stock Entry", {
    refresh(frm) {
        frm.set_query("stock_entry_type", () => {
            return {
                filters: {
                    name: ["in", ["Material Issue", "Material Receipt", "Material Transfer"]]
                }
            };
        });
    }
});
