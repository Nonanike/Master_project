import maya.cmds as cmds

class PaintTab():

    def paintTool(self, R,G,B,A):
        # Activate the vertex color painting tool
        cmds.PaintVertexColorTool()
        # Modify the color value of the painting context
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(),e = True, colorRGBAValue = (R, G, B, A ))

    def exitPaintTool(self):
        
        cmds.setToolTo("selectSuperContext")