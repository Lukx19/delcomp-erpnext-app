

def combine_conditions(conditions):
	if conditions == "":
		conditions += "WHERE"
	else:
		conditions += "AND"
	return conditions
