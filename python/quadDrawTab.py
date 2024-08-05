import maya.cmds as cmds
import maya.mel as Mmmesh


class quadDrawTab():
    
    def duplicateMesh(self):
        
        self.mesh = cmds.ls(sl=True, fl=True)

        cmds.select(self.mesh)
   
        duplicated = cmds.duplicate(name="duplicated")

        cmds.select(clear = True)
        cmds.select(self.mesh)

        cmds.createDisplayLayer(name="display")

        cmds.setAttr("display.displayType", 2)
        cmds.setAttr("display.visibility", 0)

        cmds.select(duplicated)
        return duplicated

    def quadDrawTool(self):

        duplicated = self.duplicateMesh()
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

        cmds.select(self.mesh)
        cmds.scale(0.9, 0.9, 0.9)
        cmds.translate()
        # cmds.select("polySurface1")
