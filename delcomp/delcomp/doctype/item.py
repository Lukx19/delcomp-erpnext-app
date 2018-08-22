from __future__ import unicode_literals

import frappe
import json

from frappe import _

def get_uom_line(table, uom):
    for row in table:
        if row.uom == uom:
            return row
    return None

def set_uom_value(doc, uom, val):
    row = get_uom_line(doc.uoms, uom)
    if row == None:
        row = doc.append("uoms",{})
    row.uom = uom
    row.conversion_factor = val

def gen_UOM(doc, method):
    frappe.errprint("gen")
    # set length value if variant is used
    if doc.variant_attribute:
        for row in doc.attributes:
            if row.attribute == doc.variant_attribute and row.attribute_value:
                doc.length = int(row.attribute_value)
                break

    if not (doc.length and doc.width and doc.height):
        return

    if doc.stock_uom == "ks":
        m3 = doc.length * doc.width * doc.height / 1000000000
        m2 = doc.length * doc.width / 1000000
        set_uom_value(doc, "bm", doc.length / 1000)
        set_uom_value(doc, "m3", m3)
        set_uom_value(doc, "m2", m2)
        doc.weight_per_unit = m3 * doc.density
    if doc.stock_uom == "bm":
        m3 = 1000 * doc.width * doc.height / 1000000000
        m2 = 1000 * doc.width / 1000000
        set_uom_value(doc, "ks", doc.length / 1000)
        set_uom_value(doc, "m3", m3)
        set_uom_value(doc, "m2", m2)
        doc.weight_per_unit = m3 * doc.density


