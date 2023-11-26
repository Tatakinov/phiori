import sys, os
import json, bson

class LiveDict(dict):
	"""
	a dictionary that to export as file in real-time.
	"""
	
	def __init__(self, file, *args, **kwargs):
		self.filename = file
		if os.path.exists(file):
			with open(self.filename, "r", encoding=sys.getdefaultencoding()) as f:
				self.update(eval(f.read()))
		else:
			self.clear()
			self.update(*args, **kwargs)
	
	def _live(func):
		def wrap(self, *args, **kwargs):
			try:
				result = func(self, *args, **kwargs)
				with open(self.filename, "w", encoding=sys.getdefaultencoding()) as f:
					f.write(self.__str__())
			except:
				pass
			return result
		return wrap
	
	__setitem__ = _live(dict.__setitem__)
	__delitem__ = _live(dict.__delitem__)
	clear = _live(dict.clear)
	pop = _live(dict.pop)
	popitem = _live(dict.popitem)
	setdefault = _live(dict.setdefault)
	update = _live(dict.update)

class LiveJsonDict(dict):
	"""
	a dictionary that to export as json file in real-time.
	"""
	
	def __init__(self, file, *args, **kwargs):
		self.filename = file
		if os.path.exists(file):
			with open(self.filename, "r", encoding="utf-8") as f:
				self.update(json.load(f))
		else:
			self.clear()
			self.update(*args, **kwargs)
	
	def _live(func):
		def wrap(self, *args, **kwargs):
			try:
				result = func(self, *args, **kwargs)
				with open(self.filename, "w", encoding="utf-8") as f:
					json.dump(self, f, ensure_ascii=False, sort_keys=True, indent=4)
				return result
			except:
				pass
		return wrap
	
	__setitem__ = _live(dict.__setitem__)
	__delitem__ = _live(dict.__delitem__)
	clear = _live(dict.clear)
	pop = _live(dict.pop)
	popitem = _live(dict.popitem)
	setdefault = _live(dict.setdefault)
	update = _live(dict.update)

class LiveBsonDict(dict):
	"""
	a dictionary that to export as bson file in real-time.
	"""
	
	def __init__(self, file, *args, **kwargs):
		self.filename = file
		if os.path.exists(file):
			with open(self.filename, "rb") as f:
				self.update(bson.parse_stream(f))
		else:
			self.clear()
			self.update(*args, **kwargs)
	
	def _live(func):
		def wrap(self, *args, **kwargs):
			try:
				result = func(self, *args, **kwargs)
				with open(self.filename, "wb") as f:
					bson.serialize_to_stream(self, f)
				return result
			except:
				pass
		return wrap
	
	__setitem__ = _live(dict.__setitem__)
	__delitem__ = _live(dict.__delitem__)
	clear = _live(dict.clear)
	pop = _live(dict.pop)
	popitem = _live(dict.popitem)
	setdefault = _live(dict.setdefault)
	update = _live(dict.update)

class LivePersonaDict(dict):
	"""
	a dictionary that to export as fake-personaware setting file in real-time.
	"""
	
	def __init__(self, file, *args, **kwargs):
		self.filename = file
		if os.path.exists(file):
			with open(self.filename, "r", encoding="utf-8") as f:
				temp = {}
				lines = f.read().replace("\r", "").split("\n")
				for line in lines:
					line = line.strip()
					if not line:
						continue
					if line.startswith("#"):
						continue
					kv = line.split(",", 1)
					if len(kv) == 2:
						k, v = kv
						if temp.get(k.strip()) is None:
							temp[k.strip()] = v.strip()
						elif isinstance(temp[k.strip()], list):
							temp[k.strip()].append([temp[k.strip()], v.strip()])
						elif isinstance(temp[k.strip()], set):
							temp[k.strip()].add([temp[k.strip()], v.strip()])
						elif isinstance(temp[k.strip()], tuple):
							temp[k.strip()] += ([temp[k.strip()], v.strip()], )
						else:
							temp[k.strip()] = [temp[k.strip()], v.strip()]
				self.update(temp)
		else:
			self.clear()
			self.update(*args, **kwargs)
	
	def _live(func):
		def wrap(self, *args, **kwargs):
			try:
				result = func(self, *args, **kwargs)
				with open(self.filename, "w", encoding="utf-8") as f:
					for k, v in self.items():
						if isinstance(v, list) or isinstance(v, tuple) or isinstance(v, set):
							for i in v:
								f.write(str(k) + "," + str(i) + "\n")
						else:
							f.write(str(k) + "," + str(v) + "\n")
				return result
			except:
				pass
		return wrap
	
	__setitem__ = _live(dict.__setitem__)
	__delitem__ = _live(dict.__delitem__)
	clear = _live(dict.clear)
	pop = _live(dict.pop)
	popitem = _live(dict.popitem)
	setdefault = _live(dict.setdefault)
	update = _live(dict.update)

class PropertyDict(dict):
	"""
	a dictionary that to use items as property.
	"""
	
	def __init__(self, *args, **kwargs):
		super(PropertyDict, self).__init__(*args, **kwargs)
		self.__dict__ = self
