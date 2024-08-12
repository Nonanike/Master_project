import maya.cmds as cmds
import maya.mel as Mm

class quadDrawTab():

    copied = False

    def saveMesh(self):
        """Saves selcted mesh as self. mesh and assigns it color

        Return: self.mesh
        """
        self.mesh = cmds.ls(sl=True, fl=True)
        print(self.mesh)

        cmds.select(clear = True)
        cmds.select(self.mesh)

        cmds.polyColorPerVertex( rgb=(0.4, 0.4, 0.4) )

        return self.mesh
    
    def duplicateMesh(self):
        """
        Creates a duplicate of the saved mesh and puts 
        the orignal geometry on a display layer while setting it 
        to be invisible and unelectable
        
        Return: self.duplicated
        """
        self.mesh = cmds.ls(sl=True, fl=True)

        cmds.select(self.mesh)
   
        self.duplicated = cmds.duplicate(name="duplicated")

        cmds.select(clear = True)
        cmds.select(self.mesh)

        cmds.createDisplayLayer(name="display")

        cmds.setAttr("display.displayType", 2)
        cmds.setAttr("display.visibility", 0)

        cmds.select(self.duplicated)
        return self.duplicated

    def quadDrawTool(self):
        """
        Calls on duplicateMesh and then makes the duplicate live
        in order to use QuadDraw Tool
        """
        duplicated = self.duplicateMesh()
        cmds.select(duplicated)

        # Make the object live
        cmds.makeLive()
        
        cmds.QuadDrawTool()
        cmds.nexQuadDrawCtx()
              
    def deleteDuplicated(self):
        """
        Deletes the duplicate and the display layer
        created in duplicateMesh
        """
        cmds.makeLive(none=True)

        cmds.setToolTo("selectSuperContext")

        cmds.select("duplicated")
        cmds.delete("duplicated")

        Mm.eval("layerEditorDeleteLayer display")

        quadDrawTab.copied == True
        self.deleteCopyColor()

        cmds.select(self.mesh)
        cmds.scale(0.9, 0.9, 0.9)

        Mm.eval("maintainActiveChangeSelectMode pSphere1 0;")
        cmds.select("polySurface1")

    def mirror(self):
        """
        Calls on mirror function from Maya
        """
        self.mesh = cmds.ls(sl=True, fl=True)
        cmds.select(self.mesh)
        cmds.MirrorPolygonGeometry()
        cmds.setAttr("polyMirror1.axisDirection", 0)

    def colorCopyMesh(self):
        """Creates copy of the saved mesh and 
        puts it on the display layer to make it visible but unelectable

        Return: self.colorCopy
        """
        cmds.select(self.mesh)
   
        self.colorCopy = cmds.duplicate(name="colorCopy")

        cmds.select(self.colorCopy)

        cmds.createDisplayLayer(name="color_copy")

        cmds.setAttr("color_copy.displayType", 2)

        cmds.select(self.colorCopy)
        return self.colorCopy

    def groupAndCopyVertices(self, color):
        """
        Selects all the vertices of the saved mesh and iterates 
        through each of them to group based on their assigned color values
        """
        cmds.select(self.colorCopy)

        # if selection:
        mesh = self.colorCopy[0]
        # Get the vertices of the mesh
        vertices = cmds.ls(mesh + ".vtx[*]", fl=True)

        # Group for each color
        group = []

        # Get the colour info of each vertex
        for vertex in vertices:
            colorVal = cmds.polyColorPerVertex(vertex, query=True, rgb=True)

            if colorVal == color:
                group.append(vertex)

            cmds.select(group)
            cmds.ConvertSelectionToFaces()

    def quadToolColor(self, R, G, B):
        """
        Calls deleteCopyColor and groupAndCopyVertices to delete the selected faces 
        of the copied mesh in a chosen color, colors the rest in rgb=(0.4, 0.4, 0.4)
        and scales it up a bit in order to allow the user to only focus on their chosen color
        """
        self.deleteCopyColor()
        
        copyColor = self.colorCopyMesh()
        cmds.select(copyColor)
        self.groupAndCopyVertices([R,G,B])
        cmds.delete()
        cmds.select(copyColor)
        cmds.polyColorPerVertex( rgb=(0.4, 0.4, 0.4) )
        cmds.scale(1.01,1.01,1.01)
        cmds.select(self.mesh)

        quadDrawTab.copied = True
                
    def deleteCopyColor(self):
        """
        Checks if there is already copied mesh "colorCopy"
        and if that is true then it deletes it and sets
        the condition to False
        """

        if quadDrawTab.copied == True:

            cmds.select("colorCopy")

            cmds.delete("colorCopy")

            Mm.eval("layerEditorDeleteLayer color_copy")

            quadDrawTab.copied = False

        else:
            pass