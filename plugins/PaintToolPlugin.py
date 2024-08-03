import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI1
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


from paintRetoTool import MayaPaintToolDialog

'''
def maya_useNewAPI():
    """
    Can either use this function (which works on earlier versions)
    or we can set maya_useNewAPI = True
    """
    pass
'''

maya_useNewAPI = True

paintTool_dialog = None

def MayaPaintToolUIScript(restore = False ) :
    global paintTool_dialog
    if restore == True :
        restored_control = OpenMayaUI1.MQtUtil.getCurrentParent()
    if paintTool_dialog is None :
        print("creating new ui")
        paintTool_dialog = MayaPaintToolDialog()
        paintTool_dialog.setObjectName('MayaPaintTool')
    if restore == True :
        mixin_ptr = OpenMayaUI1.MQtUtil.findControl(paintTool_dialog.objectName())
        OpenMayaUI1.MQtUtil.addWidgetToMayaLayout(int(mixin_ptr),int(restored_control))
    else :
        paintTool_dialog.show(dockable=True,width=600,height=400, uiScript='MayaPaintToolUIScript(restore=True)')

class MayaPaintTool(om.MPxCommand):

    CMD_NAME = "MayaPaintTool"

    def __init__(self):
        super(MayaPaintTool, self).__init__()

    def doIt(self, args):
        ui = MayaPaintToolUIScript()
        if ui is not None :
            try :
                cmds.workspaceControl('MayaPaintToolWorkspaceControl', e=True, restore=True)

            except :
                pass
        return ui

    @classmethod
    def creator(cls):
        """
        Think of this as a factory
        """
        return MayaPaintTool()


def initializePlugin(plugin):
    """
    Load our plugin
    """
    vendor = "NCCA"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(MayaPaintTool.CMD_NAME, MayaPaintTool.creator)
    except:
        om.MGlobal.displayError(
            "Failed to register command: {0}".format(MayaPaintTool.CMD_NAME)
        )


def uninitializePlugin(plugin):
    """
    Exit point for a plugin
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(MayaPaintTool.CMD_NAME)
    except:
        om.MGlobal.displayError(
            "Failed to deregister command: {0}".format(MayaPaintTool.CMD_NAME)
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
