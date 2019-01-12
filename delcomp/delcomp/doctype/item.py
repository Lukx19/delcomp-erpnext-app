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
    # frappe.errprint("gen")
    # set length value if variant is used
    if doc.variant_attribute:
        for row in doc.attributes:
            if row.attribute == doc.variant_attribute and row.attribute_value:
                doc.length = int(row.attribute_value)
                break

    if not (doc.length and doc.width and doc.height):
        return
    if doc.stock_uom == "ks":
        #  calculate how many "ks" is one "bm" of goods
        m3 = doc.length * doc.width * doc.height / 1000000000
        m2 = doc.length * doc.width / 1000000
        set_uom_value(doc, "bm", 1/(doc.length / 1000))
        set_uom_value(doc, "m3", 1/m3)
        set_uom_value(doc, "m2", 1/m2)
        doc.weight_per_unit = m3 * doc.density
    if doc.stock_uom == "bm":
        m3 = 1000 * doc.width * doc.height / 1000000000
        m2 = 1000 * doc.width / 1000000
        set_uom_value(doc, "ks", doc.length / 1000)
        set_uom_value(doc, "m3", m3)
        set_uom_value(doc, "m2", m2)
        doc.weight_per_unit = m3 * doc.density


def calculate_price(doc, method):
    if not doc.price:
        return
    if doc.price_uom == doc.stock_uom:
        doc.valuation_rate = doc.price
    else:
        uom_conversion = get_uom_line(doc.uoms,doc.price_uom)
        if uom_conversion:
             doc.valuation_rate = doc.price / uom_conversion.conversion_factor
        else:
            frappe.throw("Prosím vyplňte tabuľku prevodov s konverzným faktorom z mernej jednotky " +doc.price_uom)


def fill_item_fields(doc, method):
    gen_UOM(doc, method)
    calculate_price(doc,method)
