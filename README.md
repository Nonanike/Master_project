## Nina Kokot

# Maya Paint and Retopology pipeline tool

## Overview

This is a plug-in for Maya Autodesk that allows the user to learn re-topology process and helps to improve the topology flow and saves time in the production pipeline.

## Requirements
* Maya Autodesk
* Python==3.0

## Deployment
1. Clone repo:

## User instructions

## Testing
In order to run tests run 

### Project structure

	/project
		/plugins
			/paintRetoToolPlugin.py
		/src
			/images
			/tests
			/exampleTab.py
			/paintRetoTool.py
			/paintTab.py
			/quadDrawTab.py
			/templateTab.py




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