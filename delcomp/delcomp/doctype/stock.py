
from erpnext.stock.get_item_details import validate_price_list,get_conversion_factor,validate_conversion_rate,insert_item_price
import frappe
import erpnext
from frappe.utils import flt

def get_price_list_rate(args, item_doc, out):
	meta = frappe.get_meta(args.parenttype or args.doctype)

	if meta.get_field("currency") or args.get('currency'):
		validate_price_list(args)
		if meta.get_field("currency") and args.price_list:
			validate_conversion_rate(args, meta)

		price_list_rate = get_price_list_rate_for(args, item_doc.name) or 0


		# variant
		if not price_list_rate and item_doc.variant_of:
			# frappe.errprint("variant"+str(item_doc.variant_of))
			price_list_rate = get_price_list_rate_for(args, item_doc.variant_of)
			# frappe.errprint("variant"+str(price_list_rate))

		if not price_list_rate:
			price_list_rate = get_price_list_rate_general(args, item_doc.name, item_doc.variant_of)
			# frappe.errprint("general" + str(price_list_rate))

		# insert in database
		if not price_list_rate:
			if args.price_list and args.rate:
				insert_item_price(args)
			return {}

		out.price_list_rate = flt(price_list_rate) * flt(args.plc_conversion_rate) \
			/ flt(args.conversion_rate)
		# frappe.errprint("res"+str(out.price_list_rate)+"   "+ str(args.plc_conversion_rate) +"   "+ str(args.conversion_rate))
		if not out.price_list_rate and args.transaction_type=="buying":
			from erpnext.stock.doctype.item.item import get_last_purchase_details
			out.update(get_last_purchase_details(item_doc.name,
				args.name, args.conversion_rate))

def get_price_list_rate_general(args, item_code, variant_template_code=None):
	item_price_args = {
			"item_code": item_code,
			"price_list": args.get('price_list'),
			"uom": "",
			"transaction_date": args.get('transaction_date'),
	}

	if variant_template_code:
		# frappe.errprint("variant set"+ str(variant_template_code))
		general_price_list_rate = get_item_price(item_price_args, item_code)
		if not general_price_list_rate:
			general_price_list_rate = get_item_price(item_price_args, variant_template_code)
	else:
		general_price_list_rate = get_item_price(item_price_args, item_code)
	# frappe.errprint("best matches"+str(general_price_list_rate))
	item_price_data = None
	conversion_factor = None

	for price_entry in general_price_list_rate:
		conversion_rate = get_conversion_factor(item_code, price_entry[2])["conversion_factor"]
		# frappe.errprint("********"+str(conversion_rate)+"   " + str(price_entry))
		if conversion_rate:
			conversion_factor = conversion_rate
			item_price_data = [price_entry]
			break
		# frappe.errprint("4" + item_code + "  " + str(general_price_list_rate) + str(conversion_factor))

	if item_price_data:
		# found uom -> stock uom -> uom
		return flt(item_price_data[0][1] * (1 / flt(conversion_factor)) * flt(args.get("conversion_factor", 1)))




def get_price_list_rate_for(args, item_code):
	"""
		Return Price Rate based on min_qty of each Item Price Rate.\
		For example, desired qty is 10 and Item Price Rates exists
		for min_qty 9 and min_qty 20. It returns Item Price Rate for qty 9 as
		the best fit in the range of avaliable min_qtyies

		:param customer: link to Customer DocType
		:param supplier: link to Supplier DocType
		:param price_list: str (Standard Buying or Standard Selling)
		:param item_code: str, Item Doctype field item_code
		:param qty: Derised Qty
		:param transaction_date: Date of the price
	"""
	item_price_args = {
			"item_code": item_code,
			"price_list": args.get('price_list'),
			"customer": args.get('customer'),
			"supplier": args.get('supplier'),
			"uom": args.get('uom'),
			"min_qty": args.get('qty'),
			"transaction_date": args.get('transaction_date'),
	}

	item_price_data = 0
	price_list_rate = get_item_price(item_price_args, item_code)
	# frappe.errprint(item_code+"  "+str(price_list_rate))
	if price_list_rate:
		desired_qty = args.get("qty")
		if check_packing_list(price_list_rate[0][0], desired_qty, item_code):
			item_price_data = price_list_rate
	else:
		for field in ["customer", "supplier", "min_qty"]:
			del item_price_args[field]

		general_price_list_rate = get_item_price(item_price_args, item_code)
		# frappe.errprint("2"+ item_code+"  "+str(general_price_list_rate))
		if not general_price_list_rate and args.get("uom") != args.get("stock_uom"):
			# BUG: changed from args to uom, stock uom not always passed in
			if args.get("stock_uom"):
				item_price_args["uom"] = args.get("stock_uom")
				general_price_list_rate = get_item_price(item_price_args, item_code)
				# frappe.errprint("3"+ item_code+"  "+str(general_price_list_rate))

		if general_price_list_rate:
			item_price_data = general_price_list_rate

	if item_price_data:
		if item_price_data[0][2] == args.get("uom"):
			return item_price_data[0][1]
		elif not args.get('price_list_uom_dependant'):
			return flt(item_price_data[0][1] * flt(args.get("conversion_factor", 1)))
		else:
			return item_price_data[0][1]

def get_item_price(args, item_code):
	"""
		Get name, price_list_rate from Item Price based on conditions
			Check if the Derised qty is within the increment of the packing list.
		:param args: dict (or frappe._dict) with mandatory fields price_list, uom
			optional fields min_qty, transaction_date, customer, supplier
		:param item_code: str, Item Doctype field item_code
	"""

	args['item_code'] = item_code
	conditions = "where (customer is null or customer = '') and (supplier is null or supplier = '')"
	if args.get("customer"):
		conditions = "where customer=%(customer)s"

	if args.get("supplier"):
		conditions = "where supplier=%(supplier)s"

	conditions += """ and item_code=%(item_code)s
		and price_list=%(price_list)s """

	if args.get("uom"):
		conditions += """ and ifnull(uom, '') in ('', %(uom)s)"""

	if args.get('min_qty'):
		conditions += " and ifnull(min_qty, 0) <= %(min_qty)s"

	if args.get('transaction_date'):
		conditions += """ and %(transaction_date)s between
			ifnull(valid_from, '2000-01-01') and ifnull(valid_upto, '2500-12-31')"""
	# frappe.errprint("++++++++++++++  custom ++++++++++++++++")
	# frappe.errprint(""" select name, price_list_rate, uom
	# 	from `tabItem Price` {conditions}
	# 	order by uom desc, min_qty desc """.format(conditions=conditions))
	# frappe.errprint(args)

	return frappe.db.sql(""" select name, price_list_rate, uom
		from `tabItem Price` {conditions}
		order by uom desc, min_qty desc """.format(conditions=conditions), args)

@frappe.whitelist()
def overridejs_get_item_details():
	erpnext.stock.get_item_details.get_price_list_rate = get_price_list_rate
	erpnext.stock.get_item_details.get_price_list_rate_for = get_price_list_rate_for
	erpnext.stock.get_item_details.get_item_price = get_item_price


def override_get_item_details(doc, method):
	# frappe.errprint("custom"+ str(method))
	overridejs_get_item_details

