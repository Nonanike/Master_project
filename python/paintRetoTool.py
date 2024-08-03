import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
# import maya.api.OpenMayaUI as OpenMayaUI
import maya.OpenMayaUI as OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.mel as Mm
#import math
import sys

# from paintTab import PaintTab

from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QApplication, QWidget,QHBoxLayout, QLabel, QSlider
import sys
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from PySide2 import QtGui


# Gets maya main window
def getMainWindow():
   window = OpenMayaUI.MQtUtil.mainWindow()
   return wrapInstance(int(window), QtWidgets.QDialog)

class MayaPaintToolDialog(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=getMainWindow()):
        super(MayaPaintToolDialog, self).__init__()

        # self.paintTab_instance = PaintTab()

        self.setWindowTitle("Paint and retopology tool")
        self.resize(500, 500)

        self.mainLayout = QtWidgets.QGridLayout()

        self.tabMenu = QtWidgets.QTabWidget()
        
        selectGeoButton = QtWidgets.QPushButton("Select Mesh First")
        selectGeoButton.clicked.connect(self.saveGeo)
      
        self.mainLayout.addWidget(selectGeoButton)

        self.mainLayout.addWidget(self.tabMenu)
        self.examplesTab()
        self.paintTab()
        self.QuadDrawTab()

        self.setLayout(self.mainLayout)

        self.geo = None
        self.copied = False

    def examplesTab(self):

        examplesTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(examplesTabBody, "Examples")

        self.examplesLayout = QtWidgets.QGridLayout()
        examplesTabBody.setLayout(self.examplesLayout)

    def paintTab(self):

        paintTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(paintTabBody, "Paint tab")

        self.paintLayout = QtWidgets.QVBoxLayout()
        paintTabBody.setLayout(self.paintLayout)

        self.brushOptions()
        self.paintOptions()

    def paintOptions(self):
        
        paintGroup = QtWidgets.QGroupBox("Choose color")

        colorLayout = QtWidgets.QVBoxLayout()
        paintGroup.setLayout(colorLayout)

        paintEraseButton = QtWidgets.QPushButton("Erase paint")
        paintEraseButton.clicked.connect(lambda : self.paintTool(0.4,0.4,0.4,1.0))

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
        
        # self.createSLider()

        colorLayout.addWidget(paintBlackButton)
        colorLayout.addWidget(paintWhiteButton)
        colorLayout.addWidget(paintEraseButton)

        self.paintLayout.addWidget(paintGroup)

    def brushOptions(self):

        brushGroup = QtWidgets.QGroupBox("Brush size")

        self.brushLayout = QtWidgets.QVBoxLayout()
        brushGroup.setLayout(self.brushLayout)

        # brushLabel = QLabel("Brush size")
        # font = brushLabel.font()
        # font.setPointSize(15)
        # brushLabel.setFont(font)
        # brushLabel.setAlignment( Qt.AlignHCenter )

        # self.brushLayout.addWidget(brushLabel)
        self.paintLayout.addWidget(brushGroup)
        
        self.createSlider()

    def createSlider(self):
        
        sliderGroup = QtWidgets.QGroupBox()

        sliderLayout = QtWidgets.QHBoxLayout()
        sliderGroup.setLayout(sliderLayout)
 
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.setMinimum(0.01)
        self.slider.setMaximum(10000.00)
        # self.slider.setGeometry(30, 40, 100, 30)
 
        self.slider.valueChanged.connect(self.changedValue)
 
        self.sliderLabel = QLabel("0.1")
        self.sliderLabel.setFont(QtGui.QFont("Sanserif", 10))
        self.sliderLabel.setGeometry(140, 40, 30, 30)

        sliderLayout.addWidget(self.sliderLabel)
        sliderLayout.addWidget(self.slider)

        self.brushLayout.addWidget(sliderGroup)

    def changedValue(self):
        size = self.slider.value() / 100.0
        self.sliderLabel.setText(str(size))
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e=True, radius = (size))
        
    def QuadDrawTab(self):
        
        QuadDrawTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(QuadDrawTabBody, "QuadDraw tab")

        QuadDrawLayout = QtWidgets.QVBoxLayout()
        QuadDrawTabBody.setLayout(QuadDrawLayout)
       
        # Black 
        QuadDrawStartButton = QtWidgets.QPushButton("START")
        QuadDrawStartButton.clicked.connect(self.quadDrawTool) 

        QuadDrawDoneButton = QtWidgets.QPushButton("DONE")
        QuadDrawDoneButton.clicked.connect(self.deleteDuplicated) 


        QuadDrawLayout.addWidget(QuadDrawStartButton)
        QuadDrawLayout.addWidget(QuadDrawDoneButton)

    def saveGeo(self):
        geo = cmds.ls(sl=True, fl=True)
        print(geo)

        cmds.select(clear = True)
        cmds.select(geo)

    def paintTool(self, R,G,B,A):
        # Activate the vertex color painting tool
        cmds.PaintVertexColorTool()
        # Modify the color value of the painting context
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(),e = True, colorRGBAValue = (R, G, B, A ))

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

if __name__ == "__main__":
   try:
       mayaPaintToolDialog.close()
       mayaPaintToolDialog.deleteLater()
   except:
       pass

   mayaPaintToolDialog = MayaPaintToolDialog()
   mayaPaintToolDialog.show()