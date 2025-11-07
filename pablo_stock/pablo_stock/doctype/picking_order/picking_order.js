// Copyright (c) 2025, Frank and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Picking Order", {
 	refresh(frm) {
create_actions(frm)
 	},

 });
function status_in_process(frm) {
  frm.call("status_in_process").then((r) => {
    frm.reload_doc();
  });
}
function status_complete(frm) {
  frm.call("status_complete").then((r) => {
    frm.reload_doc();
  });
}
function status_dispatched(frm) {
  frm.call("status_dispatched").then((r) => {
    frm.reload_doc();
  });
}
function create_actions(frm) {
  frm.page.clear_actions_menu();
  if (frm.doc.status === "Pending") {
    frm.page.add_action_item(("Start"), function () {
    status_in_process(frm)
    });
  } else if (frm.doc.status === "In Process"){
     frm.page.add_action_item(("Complete"), function () {
    status_complete(frm)
    });
  }else if (frm.doc.status === "Completed"){
     frm.page.add_action_item(("Dispatch"), function () {
    status_dispatched(frm)
    });
  }
}

