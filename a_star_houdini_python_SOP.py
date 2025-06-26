node = hou.pwd()
hou.frame()

a_star_hda = hou.node("../a_star_hda")
a_star_hda.hdaModule().updateNpcsPosition(a_star_hda)