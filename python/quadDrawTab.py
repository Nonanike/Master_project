import maya.cmds as cmds
import maya.mel as Mm


class quadDrawTab():

    def saveGeo(self):
        geo = cmds.ls(sl=True, fl=True)
        print(geo)

        cmds.select(clear = True)
        cmds.select(geo)

    def duplicateGeo(self):
        
        self.geo = cmds.ls(sl=True, fl=True)

        cmds.select(self.geo)
   
        duplicated = cmds.duplicate(name="duplicated")

        cmds.select(clear = True)
        cmds.select(self.geo)

        cmds.createDisplayLayer(name="display")

        cmds.setAttr("display.displayType", 2)
        cmds.setAttr("display.visibility", 0)

        cmds.select(duplicated)
        return duplicated

    def quadDrawTool(self):

        duplicated = self.duplicateGeo()
        cmds.select(duplicated)

        # Make the object live
        cmds.makeLive()
        
        cmds.QuadDrawTool()
        cmds.nexQuadDrawCtx()
              
    def deleteDuplicated(self):

        cmds.makeLive(none=True)

        cmds.setToolTo("selectSuperContext")

        cmds.select("duplicated")
        cmds.delete("duplicated")

        Mm.eval("layerEditorDeleteLayer display")

        cmds.select(self.geo)
        cmds.scale(0.9, 0.9, 0.9)
        cmds.translate()
