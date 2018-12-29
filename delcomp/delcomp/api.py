import frappe

@frappe.whitelist()
def get_batches_and_amounts(doctype, txt, item, warehouse,max_lines=5):
	filter_conds = ["disabled = 0","(expiry_date >= CURDATE() OR expiry_date IS NULL)"]
	txt = txt.strip()
	if len(txt) > 0:
		filter_conds.append(""" `tabBatch`.name like '{txt}'"""
							.format(txt=frappe.db.escape('%{0}%'.format(txt))))

	if item:
		filter_conds.append(" `tabBatch`.item = '{item}'".format(item=frappe.db.escape(item)))

	if warehouse:
		filter_conds.append(" `tabStock Ledger Entry`.warehouse= '{warehouse}'".format(
			warehouse = frappe.db.escape(warehouse)))


	query = """
			SELECT
				batch_id,
				sum(actual_qty) as qty
			FROM `tabBatch`
			JOIN `tabStock Ledger Entry` ON `tabBatch`.batch_id = `tabStock Ledger Entry`.batch_no
			WHERE {filters}
			GROUP BY batch_id
			HAVING qty > 0
			ORDER BY batch_id
			LIMIT {limit_rows}
			""".format(filters=" AND ".join(filter_conds),limit_rows=frappe.db.escape(max_lines))

	return frappe.db.sql(query)