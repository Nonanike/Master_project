import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
# import maya.api.OpenMayaUI as OpenMayaUI
import maya.OpenMayaUI as OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.mel as Mm
#import math
import sys

from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtGui, QtCore

# Gets maya main window
def getMainWindow():
   window = OpenMayaUI.MQtUtil.mainWindow()
   return wrapInstance(int(window), QtWidgets.QDialog)

class MayaPaintToolDialog(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=getMainWindow()):
        super(MayaPaintToolDialog, self).__init__()

        self.setWindowTitle("Paint and retopology tool")
        self.resize(500, 500)

        self.gridLayout = QtWidgets.QGridLayout()

        self.tabMenu = QtWidgets.QTabWidget()
        
        selectGeoButton = QtWidgets.QPushButton("Select Mesh First")
        selectGeoButton.clicked.connect(self.saveGeo)
      
        self.gridLayout.addWidget(selectGeoButton)
        self.gridLayout.addWidget(self.tabMenu)
        self.paintTab()
        self.QuadDrawTab()

        self.setLayout(self.gridLayout)

        self.geo = None
        self.copied = False

    def paintTab(self):

        paintTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(paintTabBody, "Paint tab")

        paintLayout = QtWidgets.QVBoxLayout()
        paintTabBody.setLayout(paintLayout)

        # Black Paint Button
        paintBlackButton = QtWidgets.QPushButton("Black")
        paintBlackButton.clicked.connect(lambda : self.paintTool(0.0,0.0,0.0,1.0))
        paintBlackButton.setStyleSheet("background-color : black")
        # paintBlackButton.setGeometry(200, 150, 100, 40) #doesn't work

        # White Paint Button
        paintWhiteButton = QtWidgets.QPushButton("White")
        paintWhiteButton.clicked.connect(lambda : self.paintTool(1.0,1.0,1.0,1.0))
        paintWhiteButton.setStyleSheet("background-color : white")
        paintWhiteButton.setStyleSheet("color : black")
        
        paintLayout.addWidget(paintBlackButton)
        paintLayout.addWidget(paintWhiteButton)
        
    def QuadDrawTab(self):
        
        QuadDrawTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(QuadDrawTabBody, "QuadDraw tab")

        QuadDrawLayout = QtWidgets.QVBoxLayout()
        QuadDrawTabBody.setLayout(QuadDrawLayout)
       
        # Black 
        QuadDrawBlackStartButton = QtWidgets.QPushButton("Black")
        QuadDrawBlackStartButton.clicked.connect(lambda : self.quadToolBlack(0.0,0.0,0.0)) 

        QuadDrawDoneButton = QtWidgets.QPushButton("DONE")
        QuadDrawDoneButton.clicked.connect(self.deleteDuplicated) 

        QuadDrawWhiteButton = QtWidgets.QPushButton("White")
        QuadDrawWhiteButton.clicked.connect(lambda : self.quadToolBlack(1.0,1.0,1.0))

        QuadDrawLayout.addWidget(QuadDrawBlackStartButton)
        QuadDrawLayout.addWidget(QuadDrawDoneButton)

        QuadDrawLayout.addWidget(QuadDrawWhiteButton)

    def saveGeo(self):
        geo = cmds.ls(sl=True, fl=True)
        print(geo)

        cmds.select(clear = True)
        cmds.select(geo)

        #Color all the vertices
        self.paintAllVertices()
    
    def duplicateGeo(self):
        
        self.geo = cmds.ls(sl=True, fl=True)

        cmds.select(self.geo)
   
        duplicated = cmds.duplicate(name="duplicated")

        cmds.select(clear = True)
        cmds.select(self.geo)

        cmds.createDisplayLayer(name="display")

        cmds.setAttr("display.displayType", 2)

        cmds.select(duplicated)
        return duplicated

    def paintAllVertices(self):
        # Check the object is selected
        selection = cmds.ls(sl=True)
        # Color all the vertices to -1.0
        cmds.polyColorPerVertex( rgb=(-1.0, -1.0, -1.0) )

    def paintTool(self, R,G,B,A):
        # Activate the vertex color painting tool
        cmds.PaintVertexColorTool()
        # Modify the color value of the painting context
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(),e = True, colorRGBAValue = (R, G, B, A ))

    def group_and_copyVertices(self, color):

        # Check the object is selected
        selection = cmds.ls(sl=True)

        if selection:
            geo = selection[0]
            # Get the vertices of the mesh
            vertices = cmds.ls(geo + ".vtx[*]", fl=True)

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
                cmds.InvertSelection()
                cmds.ConvertSelectionToFaces()


    def quadDrawTool(self):

        # Make the object live
        cmds.makeLive()
        
        cmds.QuadDrawTool()
        cmds.nexQuadDrawCtx()

    def quadToolBlack(self, R, G, B):
     
        duplicated = self.duplicateGeo()
        self.group_and_copyVertices([R,G,B])
        cmds.delete()
        cmds.select(duplicated)

        self.quadDrawTool()
              
    def deleteDuplicated(self):

        cmds.makeLive(none=True)

        cmds.setToolTo("selectSuperContext")

        cmds.select("duplicated")
        cmds.delete("duplicated")

        Mm.eval("layerEditorDeleteLayer display")

        
        cmds.select(self.geo)

if __name__ == "__main__":
   try:
       mayaPaintToolDialog.close()
       mayaPaintToolDialog.deleteLater()
   except:
       pass

   mayaPaintToolDialog = MayaPaintToolDialog()
   mayaPaintToolDialog.show()