// Copyright (c) 2025, Frank and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Picking Order", {
 	refresh(frm) {
create_actions(frm)
disabled_add_remove_rows(frm, "delivery_item")
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
frappe.ui.form.on('Items Picking', {
    item: function(frm, cdt, cdn) {
       let row = locals[cdt][cdn];
        let new_row = frm.add_child('delivery_item');
        new_row.item = row.item; 
        frm.refresh_field('delivery_item');
    },
    before_items_picking_remove: function(frm,cdt,cdn){
         let deleted_row = locals[cdt][cdn];
         let deleted_idx = deleted_row.idx;
        frm.doc.delivery_item = frm.doc.delivery_item.filter(row => row.idx !== deleted_idx);
        frm.refresh_field("delivery_item");
    }
});
function disabled_add_remove_rows(frm, table_field, value = true) {
  frm.set_df_property(table_field, "cannot_add_rows", value);
  frm.set_df_property(table_field, "cannot_delete_rows", value);
}

