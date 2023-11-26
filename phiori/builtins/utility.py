def early(dict, key, default=None):
	if key not in dict.keys():
		dict[key] = default
	return dict[key]
