import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
# import maya.api.OpenMayaUI as OpenMayaUI
import maya.OpenMayaUI as OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.mel as Mm
#import math
import sys

from paintTab import PaintTab
from quadDrawTab import quadDrawTab
from exampleTab import exampleTab

from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QApplication, QWidget,QHBoxLayout, QLabel, QSlider, QSpacerItem, QSizePolicy, QLineEdit
import sys
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Qt
from PySide2 import QtGui


# Gets maya main window
def getMainWindow():
   window = OpenMayaUI.MQtUtil.mainWindow()
   return wrapInstance(int(window), QtWidgets.QDialog)

class MayaPaintRetoToolDialog(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=getMainWindow()):
        super(MayaPaintRetoToolDialog, self).__init__()

        self.paintTab_instance = PaintTab()
        self.QuadDrawTab_instance = quadDrawTab()
        self.exampleTab_instance = exampleTab()

        self.setWindowTitle("Paint and retopology tool")
        self.resize(200, 500)

        self.mainLayout = QtWidgets.QGridLayout()

        self.tabMenu = QtWidgets.QTabWidget()

        self.allButtons = [] # A List for all buttons except for Select mesh and Create Image Plane

        # Select Mesh Button
        self.selectMeshButton = QtWidgets.QPushButton("Select Mesh")
        self.selectMeshButton.clicked.connect(self.QuadDrawTab_instance.saveMesh)
        self.selectMeshButton.clicked.connect(self.enableButtonsAfterClickSelect)

        # Select New Mesh Button
        self.selectNewMeshButton = QtWidgets.QPushButton("Choose a New Mesh")
        self.selectNewMeshButton.clicked.connect(self.diasableAllButtons)

        self.mainLayout.addWidget(self.selectMeshButton)
        self.mainLayout.addWidget(self.selectNewMeshButton)

        self.allButtons += [self.selectNewMeshButton]

        self.mainLayout.addWidget(self.tabMenu)
        self.examplesTab()
        self.paintTab()
        self.QuadDrawTab()

        self.diasableAllButtons()

        self.setLayout(self.mainLayout)

        self.mesh = None
        self.copied = False
        
    def diasableAllButtons(self):

        self.selectMeshButton.setEnabled(True)

        for button in self.allButtons:
            button.setEnabled(False)

        for colors in self.allColorButtons:
            colors.setEnabled(False)

    def enableButtonsAfterClickSelect(self):
        
        self.selectMeshButton.setEnabled(False)

        for button in self.allButtons:
            button.setEnabled(True)

        for colors in self.allColorButtons:
            colors.setEnabled(False)
            colors.hide()

    def examplesTab(self):

        examplesTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(examplesTabBody, "Examples")

        self.examplesLayout = QtWidgets.QVBoxLayout()
        examplesTabBody.setLayout(self.examplesLayout)

        self.exampleText()
        self.exampleImages()

    def exampleText(self):

        exampleTextGroup = QtWidgets.QGroupBox("Explanation")

        exampleTextLayout = QtWidgets.QGridLayout()
        exampleTextGroup.setLayout(exampleTextLayout)
        exampleTextGroup.setFixedHeight(250)

        text = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                      "Proin quis ornare augue, tincidunt vehicula risus. Aliquam semper pretium molestie."
                      "Quisque nunc elit, elementum a enim eget, dapibus tincidunt augue. Nulla sit amet dolor mollis, vehicula mauris id, eleifend sem. "
                      "Morbi bibendum pellentesque nibh vel scelerisque. Duis pellentesque mauris risus, ac mollis mi interdum ac. "
                      "Donec luctus massa est, sit amet sodales nisi pretium ut. Aliquam venenatis a tellus et iaculis. "
                      "In bibendum dolor vel ligula facilisis, at pellentesque est mattis. "
                      "Integer efficitur tortor vitae finibus ornare. Quisque consectetur vel magna quis faucibus. ")
        
        text.setFont(QtGui.QFont("Sanserif", 10))
        text.setWordWrap(True)

        exampleTextLayout.addWidget(text)

        self.examplesLayout.addWidget(exampleTextGroup)

    def exampleImages(self):

        imagesGroup = QtWidgets.QGroupBox("Examples")

        imagesLayout = QtWidgets.QGridLayout()
        imagesGroup.setLayout(imagesLayout)
        imagesGroup.setFixedHeight(300)

        # Spacer item left side
        spacerLeft = QLabel(self)   

        verticalSpacerL = QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Spacer item right side
        spacerRight = QLabel(self)   

        verticalSpacerR = QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # First ref image
        image1 = QLabel(self)
        pixmap1 = QPixmap('/home/s5325378/Desktop/masters_project/images/test.PNG')
        scaledImage1 = pixmap1.scaledToHeight(100, Qt.SmoothTransformation)
        image1.setPixmap(scaledImage1)
        image1.resize(scaledImage1.width(), scaledImage1.height())

        # First ref button 
        image1Button = QtWidgets.QPushButton("Create a reference plate")
        image1Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("/home/s5325378/Desktop/masters_project/images/test.PNG"))
        image1Button.setFixedSize(220, 50)

        # Second ref image
        image2 = QLabel(self)
        pixmap2 = QPixmap('/home/s5325378/Desktop/masters_project/images/test.jpg')
        scaledImage2 = pixmap2.scaledToHeight(100, Qt.SmoothTransformation)
        image2.setPixmap(scaledImage2)
        image2.resize(scaledImage2.width(), scaledImage2.height())

        # Second ref button 
        image2Button = QtWidgets.QPushButton("Create a reference plate")
        image2Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("/home/s5325378/Desktop/masters_project/images/test.jpg"))
        image2Button.setFixedSize(220, 50)

        imagesLayout.addWidget(spacerLeft)
        imagesLayout.addItem(verticalSpacerL, 0, 0)

        imagesLayout.addWidget(image1, 0, 1)
        imagesLayout.addWidget(image1Button, 1, 1)

        imagesLayout.addWidget(image2, 0, 2)
        imagesLayout.addWidget(image2Button, 1, 2)

        imagesLayout.addWidget(spacerRight)
        imagesLayout.addItem(verticalSpacerR, 0, 3)

        self.examplesLayout.addWidget(imagesGroup)

    def paintTab(self):

        paintTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(paintTabBody, "Paint tab")

        self.paintLayout = QtWidgets.QVBoxLayout()
        paintTabBody.setLayout(self.paintLayout)

        self.brushOptions()
        self.paintOptions()

    def paintOptions(self):
        
        paintGroup = QtWidgets.QGroupBox("Choose color")

        colorLayout = QtWidgets.QGridLayout()
        paintGroup.setLayout(colorLayout)

        # Black Paint Button
        paintBlackButton = QtWidgets.QPushButton("Black")
        paintBlackButton.clicked.connect(lambda : self.paintTab_instance.paintTool(0.0,0.0,0.0,1.0))
        paintBlackButton.setStyleSheet("background-color : black")
        paintBlackButton.setFixedSize(150, 50)

        # White Paint Button
        paintWhiteButton = QtWidgets.QPushButton("White")
        paintWhiteButton.clicked.connect(lambda : self.paintTab_instance.paintTool(1.0,1.0,1.0,1.0))
        paintWhiteButton.setStyleSheet("background-color : #FFFFFF; color : black;")
        paintWhiteButton.setFixedSize(150, 50)

        # Red Paint Button
        paintRedButton = QtWidgets.QPushButton("Red")
        paintRedButton.clicked.connect(lambda : self.paintTab_instance.paintTool(1.0,0.0,0.0,1.0))
        paintRedButton.setStyleSheet("background-color : #FF0000; color : black;")
        paintRedButton.setFixedSize(150, 50)

        # Green Paint Button
        paintGreenButton = QtWidgets.QPushButton("Green")
        paintGreenButton.clicked.connect(lambda : self.paintTab_instance.paintTool(0.0,1.0,0.0,1.0))
        paintGreenButton.setStyleSheet("background-color : #00FF00; color : black;")
        paintGreenButton.setFixedSize(150, 50)

        # Blue Paint Button
        paintBlueButton = QtWidgets.QPushButton("Blue")
        paintBlueButton.clicked.connect(lambda : self.paintTab_instance.paintTool(0.0,0.0,1.0,1.0))
        paintBlueButton.setStyleSheet("background-color : #0000FF")
        paintBlueButton.setFixedSize(150, 50)

        # Yellow Paint Button
        paintYellowButton = QtWidgets.QPushButton("Yellow")
        paintYellowButton.clicked.connect(lambda : self.paintTab_instance.paintTool(1.0,1.0,0.0,1.0))
        paintYellowButton.setStyleSheet("background-color : #FFFF00; color : black;")
        paintYellowButton.setFixedSize(150, 50)

        # Orange Paint Button
        paintOrangeButton = QtWidgets.QPushButton("Orange")
        paintOrangeButton.clicked.connect(lambda : self.paintTab_instance.paintTool(1.0,0.5,0.0,1.0))
        paintOrangeButton.setStyleSheet("background-color : #FF8900")
        paintOrangeButton.setFixedSize(150, 50)

        # Pink Paint Button
        paintPinkButton = QtWidgets.QPushButton("Pink")
        paintPinkButton.clicked.connect(lambda : self.paintTab_instance.paintTool(1.0,0.0,0.5,1.0))
        paintPinkButton.setStyleSheet("background-color : #FF00FF")
        paintPinkButton.setFixedSize(150, 50)

        # Purple Paint Button
        paintPurpleButton = QtWidgets.QPushButton("Purple")
        paintPurpleButton.clicked.connect(lambda : self.paintTab_instance.paintTool(0.5,0.0,0.5,1.0))
        paintPurpleButton.setStyleSheet("background-color : #800080")
        paintPurpleButton.setFixedSize(150, 50)

        # Erase Paint Button
        paintEraseButton = QtWidgets.QPushButton("Erase paint")
        paintEraseButton.clicked.connect(lambda : self.paintTab_instance.paintTool(0.4,0.4,0.4,1.0))
        paintEraseButton.setFixedSize(150, 50)

        # Exit the Tool Button
        paintExitButton = QtWidgets.QPushButton("Exit the Paint Tool")
        paintExitButton.clicked.connect(self.paintTab_instance.exitPaintTool)

        colorLayout.addWidget(paintBlackButton, 0, 0)
        colorLayout.addWidget(paintWhiteButton, 0, 1)
        colorLayout.addWidget(paintRedButton, 0, 2)
        colorLayout.addWidget(paintGreenButton, 1, 0)
        colorLayout.addWidget(paintBlueButton, 1, 1)
        colorLayout.addWidget(paintYellowButton, 1, 2)
        colorLayout.addWidget(paintOrangeButton, 2, 0)
        colorLayout.addWidget(paintPinkButton, 2, 1)
        colorLayout.addWidget(paintPurpleButton, 2, 2)

        colorLayout.addWidget(paintEraseButton, 3, 1)
        colorLayout.addWidget(paintExitButton, 4, 1)

        self.allButtons += [paintBlackButton, paintWhiteButton, paintRedButton, paintGreenButton, paintBlueButton, paintYellowButton, paintOrangeButton, paintPinkButton, paintPurpleButton, paintEraseButton]

        self.paintLayout.addWidget(paintGroup)

    def brushOptions(self):

        brushGroup = QtWidgets.QGroupBox("Brush size")

        self.brushLayout = QtWidgets.QVBoxLayout()
        brushGroup.setLayout(self.brushLayout)
        brushGroup.setFixedHeight(100)

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

        # self.edit = QLineEdit()
        # self.edit.setFixedSize(50,30)
        # self.edit.setText(str(self.slider.value()))
 
        self.slider.valueChanged.connect(self.changedValue)
        # self.slider.valueChanged.connect(self.changedValue)
        # self.edit.textChanged.connect(self.syncValues)
 
        self.sliderLabel = QLabel("0.01")
        self.sliderLabel.setFont(QtGui.QFont("Sanserif", 10))
        self.sliderLabel.setGeometry(140, 40, 30, 30)

        # sliderLayout.addWidget(self.edit)
        sliderLayout.addWidget(self.sliderLabel)
        sliderLayout.addWidget(self.slider)

        self.brushLayout.addWidget(sliderGroup)

    # def changedValue(self, size):

    #     size = self.sliderLabel.setText(str(self.size)) /100.0
    #     self.edit.setText(str(self.size))
    #     cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e=True, radius = (size))

    # def syncValues(self, text):
            
    #         self.size = int(text)
    #         if 0.00 <= self.size <= 100.00:
    #             self.slider.setValue(self.size)

    def changedValue(self):
        size = self.slider.value() / 100.0
        self.sliderLabel.setText(str(size))
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e=True, radius = (size))
        
    def QuadDrawTab(self):
        
        QuadDrawTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(QuadDrawTabBody, "QuadDraw tab")

        self.QuadDrawLayout = QtWidgets.QVBoxLayout()
        QuadDrawTabBody.setLayout(self.QuadDrawLayout)

        self.quadDrawTool()
        self.quadDrawText()

    def quadDrawTool(self):

        self.allColorButtons = []

        quadDrawGroup = QtWidgets.QGroupBox("QuadDraw tool")

        quadLayout = QtWidgets.QGridLayout()
        quadDrawGroup.setLayout(quadLayout)
        quadDrawGroup.setFixedHeight(200)
       
        # Start Button
        self.QuadDrawStartButton = QtWidgets.QPushButton("START")
        self.QuadDrawStartButton.clicked.connect(self.QuadDrawTab_instance.quadDrawTool) 
        self.QuadDrawStartButton.clicked.connect(self.disableSTART)
        # self.QuadDrawStartButton.clicked.connect(self.enableFocus)
        self.QuadDrawStartButton.clicked.connect(self.disableColors)
        self.QuadDrawStartButton.setFixedWidth(150)

        # Focus Button
        self.QuadFocusButton = QtWidgets.QPushButton("Focus on only one color")
        self.QuadFocusButton.setEnabled(False)
        self.QuadFocusButton.clicked.connect(self.enableColors) 

        # Black Button
        self.QuadBlackButton = QtWidgets.QPushButton("Black")
        self.QuadBlackButton.clicked.connect(lambda : self.QuadDrawTab_instance.quadToolColor(0.0,0.0,0.0)) 
        self.QuadBlackButton.setStyleSheet("background-color : black")

        # White Button
        self.QuadWhiteButton = QtWidgets.QPushButton("White")
        self.QuadWhiteButton.clicked.connect(lambda : self.QuadDrawTab_instance.quadToolColor(1.0,1.0,1.0))
        self.QuadWhiteButton.setStyleSheet("background-color : #FFFFFF; color : black;")

        # Red Button
        self.QuadRedButton = QtWidgets.QPushButton("Red")
        self.QuadRedButton.clicked.connect(lambda : self.QuadDrawTab_instance.quadToolColor(1.0,0.0,0.0))
        self.QuadRedButton.setStyleSheet("background-color : #FF0000; color : black;")

        # Green Button
        self.QuadGreenButton = QtWidgets.QPushButton("Green")
        self.QuadGreenButton.clicked.connect(lambda : self.QuadDrawTab_instance.quadToolColor(0.0,1.0,0.0))
        self.QuadGreenButton.setStyleSheet("background-color : #00FF00; color : black;")

        # Blue Button
        self.QuadBlueButton = QtWidgets.QPushButton("Blue")
        self.QuadBlueButton.clicked.connect(lambda : self.QuadDrawTab_instance.quadToolColor(0.0,0.0,1.0))
        self.QuadBlueButton.setStyleSheet("background-color : #0000FF")

        # Yellow Button
        self.QuadYellowButton = QtWidgets.QPushButton("Yellow")
        self.QuadYellowButton.clicked.connect(lambda : self.QuadDrawTab_instance.quadToolColor(1.0,1.0,0.0))
        self.QuadYellowButton.setStyleSheet("background-color : #FFFF00; color : black;")

        # Orange Button
        self.QuadOrangeButton = QtWidgets.QPushButton("Orange")
        self.QuadOrangeButton.clicked.connect(lambda : self.QuadDrawTab_instance.quadToolColor(1.0,0.5,0.0))
        self.QuadOrangeButton.setStyleSheet("background-color : #FF8900")

        # Pink Button
        self.QuadPinkButton = QtWidgets.QPushButton("Pink")
        self.QuadPinkButton.clicked.connect(lambda : self.QuadDrawTab_instance.quadToolColor(1.0,0.0,0.5))
        self.QuadPinkButton.setStyleSheet("background-color : #FF00FF")

        # Purple Button
        self.QuadPurpleButton = QtWidgets.QPushButton("Purple")
        self.QuadPurpleButton.clicked.connect(lambda : self.QuadDrawTab_instance.quadToolColor(0.5,0.0,0.5))
        self.QuadPurpleButton.setStyleSheet("background-color : #800080")

        # Done Button
        self.QuadDrawDoneButton = QtWidgets.QPushButton("DONE")
        self.QuadDrawDoneButton.clicked.connect(self.QuadDrawTab_instance.deleteDuplicated)
        self.QuadDrawDoneButton.clicked.connect(self.enableSTART)
        self.QuadDrawDoneButton.clicked.connect(self.disableColors)
        self.QuadDrawStartButton.setFixedWidth(150)

        quadLayout.addWidget(self.QuadDrawStartButton, 0, 1)
        quadLayout.addWidget(self.QuadFocusButton, 1, 1)

        quadLayout.addWidget(self.QuadBlackButton, 2, 0)
        quadLayout.addWidget(self.QuadWhiteButton, 2, 1)
        quadLayout.addWidget(self.QuadRedButton, 2, 2)
        quadLayout.addWidget(self.QuadGreenButton, 3, 0)
        quadLayout.addWidget(self.QuadBlueButton, 3, 1)
        quadLayout.addWidget(self.QuadYellowButton, 3, 2)
        quadLayout.addWidget(self.QuadOrangeButton, 4, 0)
        quadLayout.addWidget(self.QuadPinkButton, 4, 1)
        quadLayout.addWidget(self.QuadPurpleButton, 4, 2)

        quadLayout.addWidget(self.QuadDrawDoneButton, 5, 1)

        self.QuadDrawLayout.addWidget(quadDrawGroup)

        self.allButtons += [self.QuadDrawStartButton, self.QuadDrawDoneButton]
        self.allColorButtons += [self.QuadBlackButton, self.QuadWhiteButton, self.QuadRedButton, self.QuadGreenButton, self.QuadBlueButton, self.QuadYellowButton, self.QuadOrangeButton, self.QuadPinkButton, self.QuadPurpleButton]

    def enableSTART(self):
        self.QuadDrawStartButton.setEnabled(True)
        self.QuadFocusButton.setEnabled(False)

    def disableSTART(self):
        self.QuadDrawStartButton.setEnabled(False)
        self.QuadFocusButton.setEnabled(True)

    def enableColors(self):

        self.QuadFocusButton.setEnabled(False)

        for button in self.allColorButtons:
            button.show()
            button.setEnabled(True)

    def disableColors(self):

        for button in self.allColorButtons:
            button.setEnabled(False)
            button.hide()

    def quadDrawText(self):

        quadDrawTextGroup = QtWidgets.QGroupBox("Reminder")

        quadDrawTextLayout = QtWidgets.QGridLayout()
        quadDrawTextGroup.setLayout(quadDrawTextLayout)
        quadDrawTextGroup.setFixedHeight(150)

        text = QLabel("To create a new polygon, after placing 4 vertices, click ")
        text2 = QLabel("SHIFT + LEFT MOUSE")
        
        text.setFont(QtGui.QFont("Sanserif", 10))
        text.setWordWrap(True)
        text.setAlignment(Qt.AlignCenter)
        text2.setFont(QtGui.QFont("Sanserif", 10))
        text2.setWordWrap(True)
        text2.setAlignment(Qt.AlignCenter)

        quadDrawTextLayout.addWidget(text)
        quadDrawTextLayout.addWidget(text2)

        self.QuadDrawLayout.addWidget(quadDrawTextGroup)

if __name__ == "__main__":
   try:
       mayaPaintRetoToolDialog.close()
       mayaPaintRetoToolDialog.deleteLater()
   except:
       pass

   mayaPaintToolDialog = MayaPaintRetoToolDialog()
   mayaPaintToolDialog.show()