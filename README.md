# Master_project

to run it in maya:

if cmds.pluginInfo("paintRetoToolPlugin", q=True, loaded=True) :
	cmds.unloadPlugin("paintRetoToolPlugin")

try :
	del sys.modules['paintRetoTool']
except :
	pass

ctrl="MayaPaintRetoToolWorkspaceControl"

if maya.cmds.workspaceControl(ctrl, exists=True) :
	maya.cmds.workspaceControl(ctrl, edit=True, close=True)
	maya.cmds.deleteUI(ctrl, control = True)

cmds.loadPlugin("paintRetoToolPlugin")
cmds.MayaPaintRetoTool()