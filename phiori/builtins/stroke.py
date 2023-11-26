@handle("OnMouseMove")
def _stroke_mousemove(*args, **kwargs):
	phiori.temp["stroke.target"] = kwargs["Reference3"]
	early(phiori.temp, "stroke.collision", "")
	early(phiori.temp, "stroke.point", 0)
	if phiori.temp["stroke.collision"] != kwargs.get("Reference4"):
		phiori.temp["stroke.point"] = 0
		phiori.temp["stroke.collision"] = kwargs.get("Reference4")
		phiori.temp["stroke.begintime"] = time.time()
	elif phiori.temp["stroke.collision"]:
		phiori.temp["stroke.point"] += 1
		now = time.time()
		if now > phiori.temp["stroke.begintime"] + 2:
			if phiori.temp["stroke.point"] / (now - phiori.temp["stroke.begintime"]) > 16:
				phiori.temp["stroke.raise"] = True
				phiori.temp["stroke.target.active"], phiori.temp["stroke.collision.active"], phiori.temp["stroke.point.active"] = phiori.temp["stroke.target"], phiori.temp["stroke.collision"], phiori.temp["stroke.point"]
				phiori.temp["stroke.collision"] = ""
				phiori.temp["stroke.point"] = 0

@handle("OnSecondChange")
def _stroke_secondchange(*args, **kwargs):
	if phiori.temp.get("stroke.raise"):
		if int(kwargs["Reference3"]):
			yield simulate("OnStroke", phiori.temp["stroke.target.active"], phiori.temp["stroke.collision.active"], phiori.temp["stroke.point.active"])
		del phiori.temp["stroke.raise"]
		del phiori.temp["stroke.target.active"]
		del phiori.temp["stroke.collision.active"]
		del phiori.temp["stroke.point.active"]
