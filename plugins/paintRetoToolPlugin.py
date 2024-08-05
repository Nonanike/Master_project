import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI1
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


from paintRetoTool import MayaPaintRetoToolDialog

'''
def maya_useNewAPI():
    """
    Can either use this function (which works on earlier versions)
    or we can set maya_useNewAPI = True
    """
    pass
'''

maya_useNewAPI = True

paintRetoTool_dialog = None

def MayaPaintRetoToolUIScript(restore = False ) :
    global paintRetoTool_dialog
    if restore == True :
        restored_control = OpenMayaUI1.MQtUtil.getCurrentParent()
    if paintRetoTool_dialog is None :
        print("creating new ui")
        paintRetoTool_dialog = MayaPaintRetoToolDialog()
        paintRetoTool_dialog.setObjectName('MayaPaintRetoTool')
    if restore == True :
        mixin_ptr = OpenMayaUI1.MQtUtil.findControl(paintRetoTool_dialog.objectName())
        OpenMayaUI1.MQtUtil.addWidgetToMayaLayout(int(mixin_ptr),int(restored_control))
    else :
        paintRetoTool_dialog.show(dockable=True,width=600,height=400, uiScript='MayaPaintRetoToolUIScript(restore=True)')

class MayaPaintRetoTool(om.MPxCommand):

    CMD_NAME = "MayaPaintRetoTool"

    def __init__(self):
        super(MayaPaintRetoTool, self).__init__()

    def doIt(self, args):
        ui = MayaPaintRetoToolUIScript()
        if ui is not None :
            try :
                cmds.workspaceControl('MayaPaintRetoToolWorkspaceControl', e=True, restore=True)

            except :
                pass
        return ui

    @classmethod
    def creator(cls):
        """
        Think of this as a factory
        """
        return MayaPaintRetoTool()


def initializePlugin(plugin):
    """
    Load our plugin
    """
    vendor = "Nina Kokot"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(MayaPaintRetoTool.CMD_NAME, MayaPaintRetoTool.creator)
    except:
        om.MGlobal.displayError(
            "Failed to register command: {0}".format(MayaPaintRetoTool.CMD_NAME)
        )


def uninitializePlugin(plugin):
    """
    Exit point for a plugin
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(MayaPaintRetoTool.CMD_NAME)
    except:
        om.MGlobal.displayError(
            "Failed to deregister command: {0}".format(MayaPaintRetoTool.CMD_NAME)
        )


if __name__ == "__main__":
    """
    So if we execute this in the script editor it will be a __main__ so we can put testing code etc here
    Loading the plugin will not run this
    As we are loading the plugin it needs to be in the plugin path.
    """

    plugin_name = "paintRetoTool.py"

    cmds.evalDeferred(
        'if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(
            plugin_name
        )
    )
    cmds.evalDeferred(
        'if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(
            plugin_name
        )
    )
