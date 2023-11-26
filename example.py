@handle("OnFirstBoot")
def firstboot():
	write(r"\1\s0\0\s0FirstBoot Event.\e")

@handle("OnBoot")
def boot():
	write(r"\1\s0\0\s0Boot Event.\e")

@handle("OnClose")
def close(reason, *args):
	write(r"\0Close Event. reason: {}\w8\w8\e", reason)

@handle("OnGhostChanged")
def ghostchanged(name, *args):
	write(r"\0GhostChanged Event. name: {}\w8\w8\e", name)

@handle("OnGhostChanging")
def ghostchanging(name, *args):
	write(r"\0GhostChanging Event. name: {}\w8\w8\e", name)

@handle("OnWindowStateRestore")
def windowstaterestore():
	write(r"\1\s0\0\s0WindowStateRestore Event.\e")

@handle("OnSakuraDoubleClick")
def sakuradblclick(*args):
	write(r"\0")
	if args[4] == "Head":
		write("Sakura Head DoubleClick Event.")
	else:
		write(simulate("OnMenu", ""))
	write(r"\e")

@handle("OnKeroDoubleClick")
def kerodblclick():
	write(r"\1Kero DoubleClick Event.\e")

@handle("OnKasanari")
def kasanari():
	write(r"\0Kasanari Event.\e")

@handle("OnStroke")
def stroke(char, id, *args):
	write(r"\0Stroke Event. char: {}, id: {}\e", char, id)

@handle("OnMenu")
def menu(id):
	write(r"\0Menu Event. id: {}\w8\n\n", id or "(empty)")
	if not id:
		write(makemenuitem("Raise Talk Event", "OnTalk"))
		write(makemenuitem("Cancel", "OnMenu", "cancel"))
	elif id == "cancel":
		write("Cancelled.")
	write(r"\e")

@handle("OnTalk")
def talk():
	write(phiori.words["talks"])
	write(r"\e")
