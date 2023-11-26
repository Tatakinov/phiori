def escape(text):
	text = str(text)
	chars = "\\,()[]{}"
	res = ""
	for i, c in enumerate(text):
		if c in chars:
			res += "\\" + c
		else:
			res += c
	return res
_escape = escape

def event(onid, *refs):
	res = r"\![raise,{}".format(onid)
	if refs:
		res += ","
		for ref in refs:
			res += ref + ","
		res = res[:-1]
	res += "]"
	return res

def initsurface(count=2):
	res = ""
	for i in range(0, count - 1):
		if r > 1:
			res += r"\p[{}]".format(narrator)
		else:
			res += "\\" + str(narrator)
	return res

def makemenu(*args, **kwargs):
	res = ""
	items = {}
	if args:
		for arg in args:
			items[arg] = arg
	if kwargs:
		for k, v in kwargs.items():
			items[k] = v
	for k, v in items.items():
		res += makemenuitem(v, k)
	res += r"\n"
	return res

def makemenuitem(title, id=None, *args, escape=True):
	res = r"\![*]\q[{}".format(_escape(title) if escape else title)
	if id:
		res += ",{}".format(id)
	else:
		res += ",{}".format(_escape(title) if escape else title)
	if isinstance(id, str):
		if id.startswith("On"):
			res += ","
			for arg in args:
				res += (_escape(arg) if escape else arg) + ","
			res = res[:-1]
	res += r"]\n"
	return res

def say(narrator, surface=None, text=None, escape=True):
	res = ""
	if narrator > 1:
		res += r"\p[{}]".format(narrator)
	else:
		res += "\\" + str(narrator)
	if text is not None:
		if surface:
			if surface > 9:
				res += r"\s[{}]".format(surface)
			else:
				res += r"\s" + str(surface)
	else:
		text = surface
	if text:
		res += str(_escape(text) if escape else text)
	res += r"\n\n"
	return res

def wait(delay=None):
	res = r"\__w["
	if delay is None or not isinstance(delay, int):
		res += "clear"
	else:
		res += str(delay)
	res += "]"
	return res
