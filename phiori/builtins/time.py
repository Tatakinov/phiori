class Timer(object):
	
	def __init__(self, name=None, interval=0, loop=False):
		if name:
			self.name = "#timer:" + str(name)
		else:
			self.name = "#timer:{}:{:07}".format(hex(int(time.time())), random.randint(0, 9999999))
		self.interval = interval
		self.loop = loop
		self._dispose = False
		phiori.temp[self.name] = self
	
	def start(self):
		self._begin = time.time()
	
	def stop(self):
		del self._begin
	
	def __call__(self):
		if getattr(self, "_begin", None):
			if self._begin + self.interval <= time.time():
				yield simulate("OnTimerElapsed", self.name[7:], self.interval, (1 if self.loop else 0))
				if self.loop:
					self.start()
				else:
					self.stop()
					self._dispose = True
	
	@staticmethod
	def setinterval(name=None, interval=None):
		if interval is None:
			name, interval = interval, name
		timer = Timer(name, interval, True)
		timer.start()
		return timer
	
	@staticmethod
	def settimeout(name=None, delay=None):
		if delay is None:
			name, delay = delay, name
		timer = Timer(name, delay, False)
		timer.start()
		return timer

@handle("OnSecondChange")
def _time_secondchange(*args, **kwargs):
	disposal = []
	for k, v in phiori.temp.items():
		if str(k).startswith("#timer:"):
			if int(kwargs["Reference3"]):
				for d in v():
					if d:
						yield d
			if v._dispose:
				disposal.append(phiori.temp[k])
	for i in disposal:
		del i

@handle("OnMinuteChange")
def _time_minutechange(*args, **kwargs):
	now = datetime.datetime.today()
	if now.minute == 0:
		yield simulate("OnHourChange", kwargs["Reference0"], kwargs["Reference1"], kwargs["Reference2"], kwargs["Reference3"])
		if now.hour == 0:
			yield simulate("OnDayChange", kwargs["Reference0"], kwargs["Reference1"], kwargs["Reference2"], kwargs["Reference3"])
