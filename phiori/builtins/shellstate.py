@handle("OnSecondChange")
def _shellstate_secondchange(*args, **kwargs):
	early(phiori.config, "shellstate.patience", 15)
	early(phiori.temp, "shellstate.mikire.timer", 0)
	early(phiori.temp, "shellstate.kasanari.timer", 0)
	if int(kwargs["Reference1"]) == 1:
		phiori.temp["shellstate.mikire.timer"] += 1
	else:
		phiori.temp["shellstate.mikire.timer"] = 0
	if int(kwargs["Reference2"]) == 1:
		phiori.temp["shellstate.kasanari.timer"] += 1
	else:
		phiori.temp["shellstate.kasanari.timer"] = 0
	if phiori.temp["shellstate.mikire.timer"] >= int(phiori.config["shellstate.patience"]) and int(kwargs["Reference3"]) == 1:
		phiori.temp["shellstate.mikire.timer"] = 0
		yield simulate("OnMikire")
	if phiori.temp["shellstate.kasanari.timer"] >= int(phiori.config["shellstate.patience"]) and int(kwargs["Reference3"]) == 1:
		phiori.temp["shellstate.kasanari.timer"] = 0
		yield simulate("OnKasanari")
