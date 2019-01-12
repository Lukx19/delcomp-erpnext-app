import frappe
import json
from frappe.model.naming import make_autoname

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
			LEFT JOIN `tabStock Ledger Entry` ON `tabBatch`.batch_id = `tabStock Ledger Entry`.batch_no
			WHERE {filters}
			GROUP BY batch_id
			ORDER BY qty DESC
			LIMIT {limit_rows}
			""".format(filters=" AND ".join(filter_conds),limit_rows=frappe.db.escape(max_lines))

	return frappe.db.sql(query)

@frappe.whitelist()
def create_batch_entries(item_codes,batch_number_series, doctype,doctype_name):
	batch_numbers = []
	i =0
	for row_id, item_code in json.loads(item_codes).items():
		if frappe.get_value("Item",item_code,"has_batch_no"):
			batch_id = make_autoname(batch_number_series)
			batch_no = frappe.get_doc(dict(
							doctype='Batch',
							item=item_code,
							batch_id=batch_id,
							reference_doctype=doctype,
							reference_name=doctype_name)).insert().name
			batch_numbers.append((row_id,item_code,batch_no))
	return batch_numbers

#  Overrides default behavior of batch no search in delivery note

def get_batches(item_code, warehouse, qty=1, throw=False):
	batches = frappe.db.sql(
		'select batch_id, sum(actual_qty) as qty from `tabBatch` join `tabStock Ledger Entry` ignore index (item_code, warehouse) '
		'on (`tabBatch`.batch_id = `tabStock Ledger Entry`.batch_no )'
		'where `tabStock Ledger Entry`.item_code = %s and  `tabStock Ledger Entry`.warehouse = %s '
		'and (`tabBatch`.expiry_date >= CURDATE() or `tabBatch`.expiry_date IS NULL)'
		'group by batch_id '
		'order by `tabBatch`.expiry_date ASC, `tabBatch`.creation ASC',
		(item_code, warehouse),
		as_dict=True
	)

	return batches

@frappe.whitelist()
def get_batch_no(item_code, warehouse, qty=1, throw=False):
	"""
	Get batch number using First Expiring First Out method.
	:param item_code: `item_code` of Item Document
	:param warehouse: name of Warehouse to check
	:param qty: quantity of Items
	:return: String represent batch number of batch with sufficient quantity else an empty String
	"""

	batch_no = None
	batches = get_batches(item_code, warehouse, qty, throw)

	for batch in batches:
		if cint(qty) <= cint(batch.qty):
			batch_no = batch.batch_id
			break

	if not batch_no:
		frappe.msgprint(_('aaaaaaaaaaaaaaa'))
		# if throw:
		# 	raise UnableToSelectBatchError

	return batch_no