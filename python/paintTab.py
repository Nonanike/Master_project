import maya.cmds as cmds

class PaintTab():

    def paintTool(self, R,G,B,A):
        # Activate the vertex color painting tool
        cmds.PaintVertexColorTool()
        # Modify the color value of the painting context
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(),e = True, colorRGBAValue = (R, G, B, A ))

    def exitPaintTool(self):
        
        cmds.setToolTo("selectSuperContext")

    def activateSymmetry(self):

        #Activates the reflection option for brush
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e = True, reflection=True)

    def deactivateSymmetry(self):
        #Deactivates the reflection option for brush
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e = True, reflection=False)

    def symmetryAxis(self, axis):

        #Reflection axis
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e = True, ra=axis)