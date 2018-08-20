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
    if not (doc.length and doc.width and doc.height):
        return
    m3 = doc.length * doc.width * doc.height / 1000000000
    m2 = doc.length * doc.width / 1000000
    set_uom_value(doc, "m3", m3)
    set_uom_value(doc, "m2", m2)
    set_uom_value(doc,"bm",doc.length/1000)
    doc.weight_per_unit = m3 * doc.density
