import sys, os, traceback
import random, locale, time
from types import GeneratorType
from collections import Iterable
from .shiori import Shiori

class Phiori:
	
	def __init__(self):
		self.configs = {}
		self.encoding = "utf-8"
		self.handlers = {}
		self.info = {}
		self.locale = locale.getdefaultlocale()
		self.objects = {}
		self.path = None
		self.resources = {}
		self.response = None
		self.temps = {}
		self.variables = None
		self.words = None
	
	def event(self, handler, *args, **kwargs):
		try:
			# event(*, **)
			if handler.__code__.co_flags & 8 and (handler.__code__.co_flags & 4 or handler.__code__.co_argcount > 0):
				res = handler(*args, **kwargs)
			# event(**)
			elif handler.__code__.co_flags & 8:
				res = handler(**kwargs)
			# event(*)
			elif handler.__code__.co_flags & 4 or handler.__code__.co_argcount > 0:
				res = handler(*args)
			# event()
			else:
				res = handler()
			if isinstance(res, Iterable):
				for r in res:
					self.response[0] += str(r)
			elif res:
				self.response[0] += str(res)
		except:
			self.response[0] = r"\0\b2\_q{}\x\c\e".format(traceback.format_exc().replace("\\", "\\\\").replace("\n", r"\n\n[half]"))
	
	def handle(self, *events):
		def decorator(func):
			for event in events:
				if not self.handlers.get(event):
					self.handlers[event] = []
				self.handlers[event].append(func)
			def wrapper(*args, **kwargs):
				self.event(func, *args, **kwargs)
			return wrapper
		return decorator
	
	def print(self, *objects, sep=" ", end=r"\n"):
		for i, o in enumerate(objects):
			self.response[0] += str(o) + (sep if i < len(objects) - 1 else "")
		self.response[0] += end
	
	def simulate(self, name, *args):
		headers = {"ID": name}
		for i, arg in enumerate(args):
			headers["Reference" + str(i)] = arg
		request = Shiori.makerequest("phiori/ego", headers=headers)
		return process(self, request).headers.get("Value", "")
	
	def write(self, text, *args, **kwargs):
		args = list(args)
		if isinstance(text, list) or isinstance(text, tuple) or isinstance(text, set):
			text = random.choice(text)
		elif isinstance(text, dict):
			text = random.choice(text.items())
		if args:
			for i, a in enumerate(args):
				if isinstance(a, list) or isinstance(a, tuple) or isinstance(a, set):
					args[i] = random.choice(a)
				elif isinstance(a, dict):
					args[i] = random.choice(a.items())
		if kwargs:
			for k, v in kwargs.items():
				if isinstance(v, list) or isinstance(v, tuple) or isinstance(v, set):
					kwargs[k] = random.choice(v)
				elif isinstance(v, dict):
					kwargs[k] = random.choice(v.items())
		self.response[0] += text.format(*args, **kwargs)
	
	def writeline(self, text, *args, **kwargs):
		write(text + r"\n", *args, **kwargs)

def process(phiori, req):
	"""
	process the shiori request.
	"""
	res = Shiori.makeresponse(phiori.configs.get("id", ("phiori/persona", ))[0], 204)
	# make unique result id.
	resid = "#res:{}:{:07}".format(hex(int(time.time())), random.randint(0, 9999999))
	# make result buffer for print, write and writeline. (and return and yield)
	phiori.temps[resid] = [""]
	# push shiori result object to stack for Phiori.simulate method.
	if "#res.stack" not in phiori.temps:
		phiori.temps["#res.stack"] = []
	phiori.temps["#res.stack"].append(phiori.response)
	# set current response queue.
	phiori.response = phiori.temps[resid]
	# TODO: legacy support for shiori2 baseware.
	if req.method == "GET":
		key = req.headers.get("ID")
		if key:
			value = {}
			nvalue = []
			for k, v in req.headers.items():
				if k.startswith("Reference"):
					i = int(k[9:])
					value[i] = v
					while len(nvalue) <= i:
						nvalue.append(None)
					nvalue[i] = v
			phiori.info[key] = value
		res = Shiori.makeresponse(phiori.configs.get("id", ("phiori/persona", ))[0])
		if req.headers.get("ID") in phiori.handlers or req.request in phiori.handlers: # if has handler
			for handler in phiori.handlers[req.headers.get("ID")]:
				try:
					phiori.event(handler, *nvalue, **req.headers)
				except:
					phiori.response = phiori.temps["#res.stack"].pop()
					res.headers["Value"] = r"\0\b2\_q{}\x\c\e".format(traceback.format_exc().replace("\\", "\\\\").replace("\n", r"\n\n[half]"))
					return res
			if phiori.response[0]:
				res = Shiori.makeresponse(phiori.configs.get("id", ("phiori/persona", ))[0], 200)
				res.headers["Value"] = phiori.response[0]
		elif req.headers.get("ID") and req.headers.get("ID") in phiori.resources: # if is resource
			res.headers["Value"] = phiori.resources[req.headers.get("ID")]
		else: # no identifier
			res = Shiori.makeresponse(phiori.configs.get("id", ("phiori/persona", ))[0], 204)
	elif req.method == "NOTIFY":
		key = req.headers.get("ID", "")
		if key:
			value = {}
			nvalue = []
			for k, v in req.headers.items():
				if k.startswith("Reference"):
					i = int(k[9:])
					value[i] = v
					while len(nvalue) <= i:
						nvalue.append(None)
					nvalue[i] = v
			phiori.info[key] = value
			res = Shiori.makeresponse(phiori.configs.get("id", ("phiori/persona", ))[0], 204)
			if key in phiori.handlers: # if has handler
				for handler in phiori.handlers[key]:
					try:
						phiori.event(handler, *nvalue, **req.headers)
					except:
						phiori.response = phiori.temps["#res.stack"].pop()
						res.headers["Value"] = r"\0\b2\_q{}\x\c\e".format(traceback.format_exc().replace("\\", "\\\\").replace("\n", r"\n\n[half]"))
						return res
				if phiori.response[0]:
					res = Shiori.makeresponse(phiori.configs.get("id", ("phiori/persona", ))[0], 200)
					res.headers["Value"] = phiori.response[0]
	# remove temporary variables.
	del phiori.temps[resid]
	phiori.response = phiori.temps["#res.stack"].pop()
	# return shiori response object.
	return res
