frappe.ui.form.on("Item", {
	custom_generate_code: async (frm)=>{
		await addRandomCode(frm);
	}
});

frappe.ui.form.on("Item Barcode", {
	custom_print_code: async (frm, cdt, cdn)=>{
		let childFrm = locals[cdt][cdn];
		printBarCode(frm, childFrm);
	}
});


async function addRandomCode(frm){

	let code = await getRandomCode(frm);
	let newChildCode = frm.add_child("barcodes");

	newChildCode.barcode = code;
	frm.refresh_field("barcodes");

}

async function getRandomCode(frm){
	let data = await frm.call({
		method: "pablo_stock.overrides.item.generate_random_code"
	});
	return data.message;
}

async function printBarCode(frm, childFrm){

	if (!childFrm.barcode)
		frappe.throw(__("You must specify the barcode"));

    const printWindow = window.open('', '_blank');

    printWindow.document.write(`
		<html>
		<head>
			<script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js"><\/script>
			<style>
				body {
					text-align: center;
					margin-top: 30px;
				}
				svg {
					width: 250px;
					height: auto;
				}
			</style>
		</head>
		<body>
			<svg id="barcode"></svg>
			<script>
				JsBarcode("#barcode", "${childFrm.barcode}", {
					format: "CODE128",
					displayValue: true
				});
				window.onload = function() {
					window.print();
					window.onafterprint = function() { window.close(); };
				};
			<\/script>
		</body>
		</html>
	`);
	printWindow.document.close();
}