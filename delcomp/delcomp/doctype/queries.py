import frappe
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.utils import nowdate
from collections import defaultdict


def item_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	conditions = []
	frappe.errprint("testetst")
	description_cond = ''
	if frappe.db.count('Item', cache=True) < 50000:
		# scan description only if items are less than 50000
		description_cond = 'or tabItem.description LIKE %(txt)s'

	return frappe.db.sql("""select tabItem.name,
		if(length(tabItem.item_name) > 40,
			concat(substr(tabItem.item_name, 1, 40), "..."), item_name) as item_name,
		tabItem.item_group,
		if(length(tabItem.description) > 40, \
			concat(substr(tabItem.description, 1, 40), "..."), description) as decription
		from tabItem
		where tabItem.docstatus < 2
			and tabItem.disabled=0
			and (tabItem.end_of_life > %(today)s or ifnull(tabItem.end_of_life, '0000-00-00')='0000-00-00')
			and (tabItem.`{key}` LIKE %(txt)s
				or tabItem.item_code LIKE %(txt)s
				or tabItem.item_group LIKE %(txt)s
				or tabItem.item_name LIKE %(txt)s
				or tabItem.item_code IN (select parent from `tabItem Barcode` where barcode LIKE %(txt)s
				{description_cond}))
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, item_name), locate(%(_txt)s, item_name), 99999),
			idx desc,
			name, item_name
		limit %(start)s, %(page_len)s """.format(
			key=searchfield,
			fcond=get_filters_cond(doctype, filters, conditions).replace('%', '%%'),
			mcond=get_match_cond(doctype).replace('%', '%%'),
			description_cond = description_cond),
			{
				"today": nowdate(),
				"txt": "%%%s%%" % txt.replace(" ","%%"),
				"_txt": txt.replace("%", ""),
				"start": start,
				"page_len": page_len
			}, as_dict=as_dict)
