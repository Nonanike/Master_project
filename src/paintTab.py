import maya.cmds as cmds

class PaintTab():

    def paintTool(self, R,G,B,A):
        """
        Activates the Paint Vertex Color Tool and modifies the color
        value based on the input
        """
        # Activate the vertex color painting tool
        cmds.PaintVertexColorTool()
        # Modify the color value of the painting context
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(),e = True, colorRGBAValue = (R, G, B, A ))

    def exitPaintTool(self):
        """
        Exits Paint Vertex Color Tool
        """
        cmds.setToolTo("selectSuperContext")

    def activateSymmetry(self):
        """
        Activates the reflection option in Paint brush
        """
        #Activates the reflection option for brush
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e = True, reflection=True)

    def deactivateSymmetry(self):
        """
        Deactivates the reflection option in Paint brush
        """
        #Deactivates the reflection option for brush
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e = True, reflection=False)

    def symmetryAxis(self, axis):
        """
        Changes the axis for the reflection function based on a different input
        """
        #Reflection axis
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e = True, ra=axis)