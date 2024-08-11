import maya.cmds as cmds
import maya.mel as Mm

class quadDrawTab():

    copied = False

    def saveMesh(self):

        self.mesh = cmds.ls(sl=True, fl=True)
        print(self.mesh)

        cmds.select(clear = True)
        cmds.select(self.mesh)

        cmds.polyColorPerVertex( rgb=(0.4, 0.4, 0.4) )

        return self.mesh
    
    def duplicateMesh(self):
        
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

        quadDrawTab.copied == True
        self.deleteCopyColor()

        cmds.select(self.mesh)
        cmds.scale(0.9, 0.9, 0.9)
        # cmds.translate()
        Mm.eval("maintainActiveChangeSelectMode pSphere1 0;")
        cmds.select("polySurface1")

############

    def colorCopyMesh(self):

        # self.mesh = cmds.ls(sl=True, fl=True)

        cmds.select(self.mesh)
   
        self.colorCopy = cmds.duplicate(name="colorCopy")

        # cmds.select(clear = True)
        cmds.select(self.colorCopy)

        cmds.createDisplayLayer(name="color_copy")

        cmds.setAttr("color_copy.displayType", 2)

        cmds.select(self.colorCopy)
        return self.colorCopy

    def groupAndCopyVertices(self, color):

        cmds.select(self.colorCopy)

        # if selection:
        mesh = self.colorCopy[0]
        # Get the vertices of the mesh
        vertices = cmds.ls(mesh + ".vtx[*]", fl=True)

        # Groups for each color
        group = []

        # Get the colour info of each vertex
        for vertex in vertices:
            colorVal = cmds.polyColorPerVertex(vertex, query=True, rgb=True)
            # print(f"Vertex: {vertex}, Color: {colorVal}")

            # # Grouping vertices into right groups depending on colors

            if colorVal == color:
                group.append(vertex)
                # print("group: ", group)

            cmds.select(group)
            # cmds.InvertSelection()
            cmds.ConvertSelectionToFaces()

    def quadToolColor(self, R, G, B):

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

        if quadDrawTab.copied == True:

            cmds.select("colorCopy")

            cmds.delete("colorCopy")

            Mm.eval("layerEditorDeleteLayer color_copy")

            # cmds.select(self.mesh)

            quadDrawTab.copied = False

        else:
            pass