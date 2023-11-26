@handle("OnSecondChange")
def _talk_secondchange(*args, **kwargs):
	early(phiori.temp, "talk.timer", 0)
	early(phiori.temp, "talk.interval", int(early(phiori.config, "talk.interval", 60)) + random.randint(-2, 4))
	if kwargs["Reference3"] == "1":
		phiori.temp["talk.timer"] += 1
	if phiori.temp["talk.timer"] >= phiori.temp["talk.interval"]:
		yield simulate("OnTalk")

@handle("OnTranslate")
def _talk_translate(*args, **kwargs):
	phiori.temp["talk.timer"] = 0
	phiori.temp["talk.interval"] = int(early(phiori.config, "talk.interval", 60)) + random.randint(-2, 4)
