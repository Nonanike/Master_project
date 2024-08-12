import maya.cmds as cmds
import os

class useTemplate():

    def shaderCreator(self, relPath):
        """
        Sets the mesh in ortographic view to face the front, 
        then creates new camera-based UVs with UVsCreator, creates a shader
        with the chosen template and assigns it to the mesh, 
        then changes the texture into color information with changeInfoColor
        """
        self.setOrtographicView()

        self.openUVEditor()
        self.mesh = cmds.ls(sl=True, fl=True)
        self.geo = self.mesh[0]
        cmds.select(self.geo)
        print(f"selected: {self.geo}")
        self.UVsCreator()
        cmds.ToggleUVTextureImage()
        cmds.modelEditor('modelPanel4', edit=True, displayTextures=True)

        # Creating the lambert shader
        self.myShader = cmds.shadingNode('lambert', asShader=True, name="myShader")

        # Creating file texture node
        self.myFile = cmds.shadingNode('file', asTexture=True, isColorManaged=True)

        # Creating place2dTexture
        self.myPlace2d = cmds.shadingNode('place2dTexture', asUtility=True)

        # Connecting place2dTexture to file texture node
        cmds.connectAttr(self.myPlace2d + '.coverage', self.myFile + '.coverage', f=True)
        cmds.connectAttr(self.myPlace2d + '.translateFrame', self.myFile + '.translateFrame', f=True)
        cmds.connectAttr(self.myPlace2d + '.rotateFrame', self.myFile + '.rotateFrame', f=True)
        cmds.connectAttr(self.myPlace2d + '.mirrorU', self.myFile + '.mirrorU', f=True)
        cmds.connectAttr(self.myPlace2d + '.mirrorV', self.myFile + '.mirrorV', f=True)
        cmds.connectAttr(self.myPlace2d + '.stagger', self.myFile + '.stagger', f=True)
        cmds.connectAttr(self.myPlace2d + '.wrapU', self.myFile + '.wrapU', f=True)
        cmds.connectAttr(self.myPlace2d + '.wrapV', self.myFile + '.wrapV', f=True)
        cmds.connectAttr(self.myPlace2d + '.repeatUV', self.myFile + '.repeatUV', f=True)
        cmds.connectAttr(self.myPlace2d + '.offset', self.myFile + '.offset', f=True)
        cmds.connectAttr(self.myPlace2d + '.rotateUV', self.myFile + '.rotateUV', f=True)
        cmds.connectAttr(self.myPlace2d + '.noiseUV', self.myFile + '.noiseUV', f=True)
        cmds.connectAttr(self.myPlace2d + '.vertexUvOne', self.myFile + '.vertexUvOne', f=True)
        cmds.connectAttr(self.myPlace2d + '.vertexUvTwo',self.myFile + '.vertexUvTwo', f=True)
        cmds.connectAttr(self.myPlace2d + '.vertexUvThree', self.myFile + '.vertexUvThree', f=True)
        cmds.connectAttr(self.myPlace2d + '.vertexCameraOne', self.myFile + '.vertexCameraOne', f=True)
        cmds.connectAttr(self.myPlace2d + '.outUV', self.myFile +'.uv')
        cmds.connectAttr(self.myPlace2d + '.outUvFilterSize', self.myFile + '.uvFilterSize')
        
        # Connecting file node with myShader
        cmds.connectAttr(self.myFile + '.outColor', self.myShader + '.color', f=True)

        # scriptDir = os.path.dirname(os.path.abspath(__file__))
        # filePath = fPath

        # Setting the path to the file
        cmds.setAttr(self.myFile + '.fileTextureName', self.relativePath(relPath), typ="string")

        # Creating myShaderGroup
        self.mySG = cmds.sets( name='myShaderGroup', renderable=True, empty=True, noSurfaceShader=True)
       
        # Assign the myShaderGroup to myShader
        cmds.connectAttr(self.myShader + '.outColor', self.mySG + ".surfaceShader")

        # Assign the shader to the mesh
        cmds.select(self.geo)
        
        cmds.sets(self.geo, e=True, forceElement= self.mySG)

        # Changing the texture to the color information
        self.changeColorInfo()

    def UVsCreator(self):
        """
        Delates UVs if any and creates a new camera-based one
        """
        cmds.select(self.geo)
        cmds.hilite(self.geo)
        cmds.select(f"{self.geo}.f[*]", add=True)
        cmds.DeleteUVs()
        cmds.select(self.geo)

        cmds.UVCameraBasedProjection()

    def adjustUVs(self):
        """
        Selects and highlights the UVs faces
        to allow user to reajust them
        """
        
        self.mesh = cmds.ls(sl=True, fl=True)
        self.geo = self.mesh[0]
        cmds.select(self.geo)
        cmds.hilite(self.geo)
        cmds.select(f"{self.geo}.f[*]", add=True)

    def setOrtographicView(self):
        """
        Sets the view into ortographic view
        and switches to the front camera
        """
        
        cmds.modelPanel('modelPanel4', edit=True, camera='front')
        cmds.camera('front', edit=True, orthographic=True)

    def openUVEditor(self):
        """
        Opens UV Editor in Maya
        """
        
        cmds.TextureViewWindow()

    # Converting texture into vertex color    
    def changeColorInfo(self):
        """
        Converts texture from shader into vertex color information
        """
        cmds.polyColorSet(self.geo, create=True, colorSet="fromTexture", representation='RGBA')

        cmds.transferAttributes(self.geo, self.geo, transferPositions= 0, transferNormals= 0, transferUVs=2, transferColors=2, sampleSpace=0, sourceUvSpace="map1", targetUvSpace="map1", searchMethod=3, flipUVs=0, colorBorders=1)

        cmds.select(self.geo)
        cmds.polyColorPerVertex(rgb=True)
        cmds.polyTransfer(self.geo, vc=True)

    def doneTemplate(self):
        """
        Switches to the perspective camera and sets current
        tool in selection mode
        """
        cmds.modelPanel('modelPanel4', edit=True, camera='persp')
        cmds.setToolTo("selectSuperContext")

    def selectObjectMode(self):
        """
        Sets the current tool to select context
        and switches to the perspective camera
        and changing the selection mode into object
        """
        cmds.select(clear = True)
        cmds.setToolTo("selectSuperContext")
        cmds.resetTool("selectSuperContext")

        cmds.modelPanel('modelPanel4', edit=True, camera='persp')

        cmds.selectType(objectComponent=True)
        cmds.selectMode(object=True)

    def relativePath(self, relPath):
        """
        Finds the current path and combines it with 
        the provided relative path to create a filePath
        
        Return: filePath
        """
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(scriptDir, relPath)

        return filePath
