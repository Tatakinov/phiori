import sys, os, traceback
import datetime, json, random, re, time, urllib.request, urllib.parse
from .shiori import *
from .phiori import *
from .collections import LiveDict, LiveJsonDict, LiveBsonDict, LivePersonaDict, PropertyDict

# on ssp, all phiori use the shared memory,
# so need to separate the namespace per ghost.
personae = {}

# activated ghost
persona = None

def load(path):
	"""
	when phiori is loaded for the first time, it will be called from the baseware.
	
	calling this method in manually is not recommended.
	"""
	global persona
	persona = None
	personae["temp"] = Phiori()
	phiori = personae["temp"]
	phiori.path = path
	phiori.configs = LivePersonaDict(os.path.join(path, "config.txt"))
	phiori.resources = LivePersonaDict(os.path.join(path, "resource.txt"))
	phiori.variables = LiveBsonDict(os.path.join(path, "variable.dat"))
	phiori.words = LiveJsonDict(os.path.join(path, "words.dic"))
	phiori.encoding = phiori.configs.get("encoding", "utf-8")
	phiori.objects = {
		#phiori variables
		"phiori": PropertyDict({
			"config": phiori.configs,
			"encoding": phiori.encoding,
			"info": phiori.info,
			"locale": phiori.locale,
			"path": path,
			"res": phiori.resources,
			"temp": phiori.temps,
			"var": phiori.variables,
			"words": phiori.words,
		}),
		#imports
		"datetime": datetime,
		"json": json,
		"os": os,
		"random": random,
		"re" : re,
		"sys": sys,
		"time": time,
		"urllib": urllib,
		#phiori functions
		"handle": phiori.handle,
		"print": phiori.print,
		"simulate": phiori.simulate,
		"write": phiori.write,
		"writeline": phiori.writeline,
	}
	#alternatives
	phiori.objects["_"] = phiori.objects["phiori"]
	phiori.objects["P"] = phiori.objects["phiori"]
	#initialise boot-time error log variables.
	phiori.temps["_boot"] = {}
	phiori.temps["_boot"]["loaderr"] = []
	#handlers for changing ghost on ssp.
	phiori.handle("OnCacheSuspend")(_oncachesuspend)
	phiori.handle("ownerghostname")(_ownerghostname)
	#load all builtin modules. ("PATH/phiori/builtins/*.py")
	# it does not allow compiled python scripts.
	for filename in os.listdir(os.path.join(path, "phiori", "builtins")):
		if os.path.splitext(filename)[1] == ".py":
			try:
				with open(os.path.join(path, "phiori", "builtins", filename), "r", encoding=phiori.encoding) as f:
					module = compile(f.read(), os.path.join(path, "phiori", "builtins", filename), "exec")
					exec(module, phiori.objects)
			except:
				phiori.temps["_boot"]["loaderr"].append(r"Error has occurred while loading builtin modules.\n\n" + r"{}".format(traceback.format_exc().replace("\\", "\\\\").replace("\n", r"\n\n[half]")))
	#load all user modules. ("PATH/*.py")
	# it does not allow compiled python scripts.
	for filename in os.listdir(path):
		if os.path.splitext(filename)[1] == ".py":
			try:
				with open(os.path.join(path, filename), "r", encoding=phiori.encoding) as f:
					module = compile(f.read(), os.path.join(path, filename), "exec")
					exec(module, phiori.objects)
			except:
				phiori.temps["_boot"]["loaderr"].append(r"Error has occurred while loading user modules.\n\n" + r"{}".format(traceback.format_exc().replace("\\", "\\\\").replace("\n", r"\n\n[half]")))
	return True

def unload():
	"""
	when phiori is unloaded, it will be called from the baseware.
	
	calling this method in manually is not recommended.
	"""
	global persona
	del parsonae[persona]
	parsonae["temp"] = Phiori()
	persona = None
	return True

def request(req):
	"""
	when baseware sent request, it will be called.
	
	calling this method in manually is not recommended.
	"""
	req = Shiori.fromrequest(req)
	res = process(personae[persona or "temp"], req)
	return str(res).encode(res.headers.get("Charset", personae[persona or "temp"].encoding))

def _oncachesuspend(**kwargs):
	global persona
	phiori = personae[persona or "temp"]
	personae["temp"] = Phiori()
	personae["temp"].handle("OnCacheSuspend")(_oncachesuspend)
	personae["temp"].handle("ownerghostname")(_ownerghostname)
	persona = None

def _ownerghostname(name, **kwargs):
	global persona
	if personae.get(name):
		old = personae[name]
		new = personae["temp"]
		old.info.update(new.info)
	else:
		personae[name] = personae["temp"]
	persona = name
