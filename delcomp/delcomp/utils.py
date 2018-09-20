

def combine_conditions(conditions):
	if conditions == "":
		conditions += "WHERE"
	else:
		conditions += "AND"
	return conditions

def combine_conditions(conditions,condition):
	if conditions == "":
		conditions += "WHERE "
	else:
		conditions += " AND "
	conditions +=condition
	return conditions
