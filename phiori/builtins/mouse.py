@handle("OnMouseClick")
def _mouse_mouseclick(*args, **kwargs):
	if not kwargs.get("Status"):
		if int(kwargs["Reference3"]) == 0:
			yield simulate("OnSakuraClick", kwargs["Reference0"], kwargs["Reference1"], kwargs["Reference2"], kwargs["Reference3"], kwargs["Reference4"], kwargs["Reference5"])
		elif int(kwargs["Reference3"]) == 1:
			yield simulate("OnKeroClick", kwargs["Reference0"], kwargs["Reference1"], kwargs["Reference2"], kwargs["Reference3"], kwargs["Reference4"], kwargs["Reference5"])
		else:
			yield simulate("OnCharacterClick", kwargs["Reference0"], kwargs["Reference1"], kwargs["Reference2"], kwargs["Reference3"], kwargs["Reference4"], kwargs["Reference5"])

@handle("OnMouseDoubleClick")
def _mouse_mousedoubleclick(*args, **kwargs):
	if not kwargs.get("Status"):
		if int(kwargs["Reference3"]) == 0:
			yield simulate("OnSakuraDoubleClick", kwargs["Reference0"], kwargs["Reference1"], kwargs["Reference2"], kwargs["Reference3"], kwargs["Reference4"], kwargs["Reference5"])
		elif int(kwargs["Reference3"]) == 1:
			yield simulate("OnKeroDoubleClick", kwargs["Reference0"], kwargs["Reference1"], kwargs["Reference2"], kwargs["Reference3"], kwargs["Reference4"], kwargs["Reference5"])
		else:
			yield simulate("OnCharacterDoubleClick", kwargs["Reference0"], kwargs["Reference1"], kwargs["Reference2"], kwargs["Reference3"], kwargs["Reference4"], kwargs["Reference5"])
