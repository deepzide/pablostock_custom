// Copyright (c) 2025, Frank and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Change Price", {
 	refresh(frm) {
create_actions(frm)
 	},
 });
function status_finished(frm) {
  frm.call("status_finished").then((r) => {
    frm.reload_doc();
  });
}
 function create_actions(frm) {
  frm.page.clear_actions_menu();
  if (frm.doc.status === "In Progress") {
    frm.page.add_action_item(("Finished"), function () {
    status_finished(frm)
    });
  } 
}