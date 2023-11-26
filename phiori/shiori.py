import sys, os, locale
from collections import OrderedDict

# parsing shiori on the basis of these documents.
# - http://usada.sakura.vg/contents/shiori.html
# - http://usada.sakura.vg/contents/specification2.html
class _Shiori:
	
	VERSION = NotImplemented
	
	def __init__(self, type):
		"""
		initialise empty shiori object.
		this method is called by methods below.
		
		- Shiori.fromrequest(req, encoding=None)
		- Shiori.makerequest(sender, method="GET", headers={}, content="", encoding="utf-8")
		- Shiori.makeresponse(sender, code=200, headers={}, content="", encoding="utf-8")
		"""
		if type not in ["request", "response"]:
			raise ValueError("type must be 'request' or 'response'")
		self.type = type
	
	@classmethod
	def fromrequest(cls, req, encoding=None):
		"""
		serialise shiori request.
		"""
		# if encoding is not specified, get encoding from shiori request.
		if not encoding:
			_req = cls.fromrequest(req, "ascii")
			encoding = _req.headers.get("Charset", locale.getdefaultlocale()[1])
			del _req
		req = req.decode(encoding, "replace")
		lines = req.split("\r\n")
		# first line defines protocol.
		line = lines[0]
		shiori = cls("request")
		# <METHOD> [<ID ...>] <VERSION>
		parts = line.split(" ")
		shiori.method, shiori.request, shiori.version = parts[0], " ".join(parts[1:-1]), parts[-1]
		shiori.headers = OrderedDict()
		i = 0
		# next lines until empty line are headers.
		for line in lines[1:]:
			i += 1
			if not line:
				break
			kv = line.split(":", 1) # key: value
			if len(kv) < 2:
				continue
			k, v = kv
			shiori.headers[k] = v[1:] # FIXME
		i += 1
		shiori.content = ""
		if len(lines) < i:
			shiori.content = "\r\n".join(lines[i:])
		# i had thought shiori protocol has content like http...
		return shiori
	
	@classmethod
	def makerequest(cls, sender, method="GET", request=None, headers={}, content="", encoding="utf-8"):
		"""
		make new shiori request object.
		"""
		shiori = cls("request")
		shiori.method = method
		shiori.request = request or ""
		shiori.version = cls.VERSION
		shiori.headers = OrderedDict({
			"Charset": encoding,
			"Sender": sender,
			"SecurityLevel": "local"
		})
		shiori.headers.update(headers)
		shiori.content = content
		return shiori
	
	@classmethod
	def makeresponse(cls, sender, code=200, headers={}, content="", encoding="utf-8"):
		"""
		make new shiori response object.
		"""
		shiori = cls("response")
		shiori.version = cls.VERSION
		shiori.code = code
		shiori.headers = OrderedDict({
			"Charset": encoding,
			"Sender": sender
		})
		shiori.headers.update(headers)
		shiori.content = content
		return shiori
	
	def __str__(self):
		"""
		deserialise shiori object.
		"""
		res = ""
		if self.type == "request":
			res = getattr(self, "method", "GET")
			if getattr(self, "request", None):
				res += " " + self.request
			res += " " + getattr(self, "version", self.VERSION)
			for k, v in self.headers.items():
				res += "\r\n{}: {}".format(k, v)
			res += "\r\n\r\n"
			if self.content:
				res += self.content
		elif self.type == "response":
			res = "{} {} {}\r\n".format(self.version, self.code, status_codes.get(self.code, "Unknown"))
			for k, v in self.headers.items():
				res += "{}: {}\r\n".format(k, v)
			res += "\r\n"
			if self.content:
				res += self.content
		return res

class Shiori3(_Shiori):
	"""
	class to serialise shiori3 protocol.
	"""
	
	VERSION = "SHIORI/3.0"

Shiori = Shiori3

# status codes from http://usada.sakura.vg/contents/shiori.html#statuscode
status_codes = {
	200: "OK",
	204: "No Content",
	310: "Communicate",
	311: "Not Enough",
	312: "Advice",
	400: "Bad Request",
	500: "Internal Server Error"
}
