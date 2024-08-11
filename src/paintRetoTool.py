import maya.cmds as cmds
# import maya.OpenMaya as OpenMaya
# import maya.api.OpenMayaUI as OpenMayaUI
import maya.OpenMayaUI as OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.mel as Mm
#import math
import sys
import os

from paintTab import PaintTab
from quadDrawTab import quadDrawTab
from exampleTab import exampleTab
from templateTab import useTemplate

from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QApplication, QWidget,QHBoxLayout, QLabel, QSlider, QSpacerItem, QSizePolicy, QLineEdit, QCheckBox
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
        self.templateTab_instance = useTemplate()

        self.setWindowTitle("Paint and retopology tool")
        self.resize(200, 500)

        self.mainLayout = QtWidgets.QGridLayout()

        self.tabMenu = QtWidgets.QTabWidget()

        self.allButtons = [] # A List for all buttons except for Select mesh and Create Image Plane

        self.selectOptions()
        self.mainLayout.addWidget(self.tabMenu)
        self.examplesTab()
        self.paintTab()
        self.templateTab()
        self.QuadDrawTab()

        self.diasableAllButtons()

        self.setLayout(self.mainLayout)

        self.mesh = None
        self.copied = False
        
    def selectOptions(self):

        selectGroup = QtWidgets.QGroupBox()

        selectLayout = QtWidgets.QGridLayout()
        selectGroup.setLayout(selectLayout)
        selectGroup.setFixedHeight(100)

        # Select Mesh Button
        self.selectMeshButton = QtWidgets.QPushButton("Select Mesh")
        self.selectMeshButton.setFixedSize(150,50)
        self.selectMeshButton.clicked.connect(self.QuadDrawTab_instance.saveMesh)
        self.selectMeshButton.clicked.connect(self.enableButtonsAfterClickSelect)

        # Select New Mesh Button
        self.selectNewMeshButton = QtWidgets.QPushButton("Choose a New Mesh")
        self.selectNewMeshButton.setFixedSize(150,50)
        self.selectNewMeshButton.clicked.connect(self.diasableAllButtons)
        self.selectNewMeshButton.clicked.connect(self.resetPaintTab)

        selectLayout.addWidget(self.selectMeshButton, 0, 0)
        selectLayout.addWidget(self.selectNewMeshButton, 0, 1)

        self.allButtons += [self.selectNewMeshButton]

        self.mainLayout.addWidget(selectGroup)

    def diasableAllButtons(self):

        self.selectMeshButton.setEnabled(True)

        for button in self.allButtons:
            button.setEnabled(False)

        for colors in self.allColorButtons:
            colors.setEnabled(False)
            colors.hide()

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

        text = QLabel("This is a tool to assist in the process of retopology using QuadDraw Tool. "
                      "Re-topology is an important part of production pipeline and if well-done can improve the process of rigging and animating a character. ")
                      
        text2 = QLabel("The proposed workflow is to use paint tool to draw the main loops and important areas directly on the mesh. "
                      "Next, when inside the QuadDraw tab and after entering the QuadDraw Tool in order to create new mesh "
                      "you need to place 4 vertices on the mesh and then SHIFT + LEFT MOUSE CLICK to create a new face. "
                      "Please use references provided underneath for guidance if needed. "
                      "They focus on the most important places on the mesh to pay attention to and show main loops to follow.")
        
        text.setFont(QtGui.QFont("Sanserif", 10))
        text.setWordWrap(True)
        text2.setFont(QtGui.QFont("Sanserif", 10))
        text2.setWordWrap(True)

        exampleTextLayout.addWidget(text)
        exampleTextLayout.addWidget(text2)

        self.examplesLayout.addWidget(exampleTextGroup)

    def relativePath(self, relPath):

        scriptDir = os.path.dirname(os.path.abspath(__file__))
        imagePath = os.path.join(scriptDir, relPath)

        return imagePath

    def exampleImages(self):

        imagesGroup = QtWidgets.QGroupBox("Examples")

        imagesLayout = QtWidgets.QGridLayout()
        imagesGroup.setLayout(imagesLayout)
        # imagesGroup.setFixedHeight(550)
        imagesGroup.setFixedSize(750, 550)

        # First ref image 
        image1 = QLabel(self)
        pixmap1 = QPixmap(self.relativePath('images/head.jpeg'))
        scaledImage1 = pixmap1.scaledToHeight(100, Qt.SmoothTransformation)
        image1.setPixmap(scaledImage1)
        image1.resize(scaledImage1.width(), scaledImage1.height())

        # First ref button 
        image1Button = QtWidgets.QPushButton("Create a reference plate")
        image1Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("images/head.jpeg"))
        image1Button.setFixedHeight(50)

        # Second ref image
        image2 = QLabel(self)
        pixmap2 = QPixmap(self.relativePath('images/headStylised.jpeg'))
        scaledImage2 = pixmap2.scaledToHeight(100, Qt.SmoothTransformation)
        image2.setPixmap(scaledImage2)
        image2.resize(scaledImage2.width(), scaledImage2.height())

        # Second ref button 
        image2Button = QtWidgets.QPushButton("Create a reference plate")
        image2Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("images/headStylised.jpeg"))
        image2Button.setFixedHeight(50)

        # Third ref image
        image3 = QLabel(self)
        pixmap3 = QPixmap(self.relativePath('images/backLines.jpeg'))
        scaledImage3 = pixmap3.scaledToHeight(100, Qt.SmoothTransformation)
        image3.setPixmap(scaledImage3)
        image3.resize(scaledImage3.width(), scaledImage3.height())

        # Third ref button 
        image3Button = QtWidgets.QPushButton("Create a reference plate")
        image3Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("images/backLines.jpeg"))
        image3Button.setFixedHeight(50)

        # Fourth ref image
        image4 = QLabel(self)
        pixmap4 = QPixmap(self.relativePath('images/front.jpeg'))
        scaledImage4 = pixmap4.scaledToHeight(100, Qt.SmoothTransformation)
        image4.setPixmap(scaledImage4)
        image4.resize(scaledImage4.width(), scaledImage4.height())

        # Fourth ref button 
        image4Button = QtWidgets.QPushButton("Create a reference plate")
        image4Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("images/front.jpeg"))
        image4Button.setFixedHeight(50)

        # Fifth ref image
        image5 = QLabel(self)
        pixmap5 = QPixmap(self.relativePath('images/arm_shoulder.jpeg'))
        scaledImage5 = pixmap5.scaledToHeight(100, Qt.SmoothTransformation)
        image5.setPixmap(scaledImage5)
        image5.resize(scaledImage5.width(), scaledImage5.height())

        # Fifth ref button 
        image5Button = QtWidgets.QPushButton("Create a reference plate")
        image5Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("images/arm_shoulder.jpeg"))
        image5Button.setFixedHeight(50)

        # Sixth ref image
        image6 = QLabel(self)
        pixmap6 = QPixmap(self.relativePath('images/hand_stylised.jpeg'))
        scaledImage6 = pixmap6.scaledToWidth(250, Qt.SmoothTransformation)
        image6.setPixmap(scaledImage6)
        image6.resize(scaledImage6.width(), scaledImage6.height())

        # Sixth ref button 
        image6Button = QtWidgets.QPushButton("Create a reference plate")
        image6Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("images/hand_stylised.jpeg"))
        image6Button.setFixedHeight(50)

        # Seventh ref image
        image7 = QLabel(self)
        pixmap7 = QPixmap(self.relativePath('images/knee.jpeg'))
        scaledImage7 = pixmap7.scaledToHeight(175, Qt.SmoothTransformation)
        image7.setPixmap(scaledImage7)
        image7.resize(scaledImage7.width(), scaledImage7.height())

        # Seventh ref button 
        image7Button = QtWidgets.QPushButton("Create a reference plate")
        image7Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("images/knee.jpeg"))
        image7Button.setFixedHeight(50)

        # Eight ref image
        image8 = QLabel(self)
        pixmap8 = QPixmap(self.relativePath('images/elbow.jpeg'))
        scaledImage8 = pixmap8.scaledToHeight(175, Qt.SmoothTransformation)
        image8.setPixmap(scaledImage8)
        image8.resize(scaledImage8.width(), scaledImage8.height())

        # Eight ref button 
        image8Button = QtWidgets.QPushButton("Create a reference plate")
        image8Button.clicked.connect(lambda : self.exampleTab_instance.createImagePlane("images/elbow.jpeg"))
        image8Button.setFixedHeight(50)

        imagesLayout.addWidget(image1, 0, 0)
        imagesLayout.addWidget(image1Button, 1, 0)

        imagesLayout.addWidget(image2, 0, 1)
        imagesLayout.addWidget(image2Button, 1, 1)

        imagesLayout.addWidget(image3, 0,2 )
        imagesLayout.addWidget(image3Button, 1, 2)

        imagesLayout.addWidget(image4, 2, 0)
        imagesLayout.addWidget(image4Button, 3, 0)

        imagesLayout.addWidget(image5, 2, 1)
        imagesLayout.addWidget(image5Button, 3,1)

        imagesLayout.addWidget(image6, 2, 2)
        imagesLayout.addWidget(image6Button, 3, 2)

        imagesLayout.addWidget(image7, 4, 0)
        imagesLayout.addWidget(image7Button, 5, 0)

        imagesLayout.addWidget(image8, 4, 1)
        imagesLayout.addWidget(image8Button, 5, 1)

        self.examplesLayout.addWidget(imagesGroup)

    def paintTab(self):
        """Holds and displays two groups:
        brushGroup  and paintGroup
        """
        paintTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(paintTabBody, "Paint tab")

        self.paintLayout = QtWidgets.QVBoxLayout()
        paintTabBody.setLayout(self.paintLayout)

        self.brushOptions()
        self.paintOptions()

    def paintOptions(self):
        """Creates a grid with paint 
        buttons and its other options
        """
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

        self.allButtons += [paintBlackButton, paintWhiteButton, paintRedButton, paintGreenButton, paintBlueButton, paintYellowButton, paintOrangeButton, paintPinkButton, paintPurpleButton, paintEraseButton, paintExitButton]

        self.paintLayout.addWidget(paintGroup)

    def brushOptions(self):
        """ 
        Group for brush options
        """
        brushGroup = QtWidgets.QGroupBox("Brush size")

        self.brushLayout = QtWidgets.QVBoxLayout()
        brushGroup.setLayout(self.brushLayout)
        brushGroup.setFixedHeight(200)

        self.paintLayout.addWidget(brushGroup)
        
        self.createSlider()
        self.activateSymmetry()

    def createSlider(self):
        """ 
        Creates a slider connected to the brush size 
        option from Paint Vertex Color Tool from Maya
        """
        sliderGroup = QtWidgets.QGroupBox()

        sliderLayout = QtWidgets.QHBoxLayout()
        sliderGroup.setLayout(sliderLayout)
 
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(0.1)
        self.slider.setSingleStep(0.1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10000)

        self.editValue = QLineEdit()
        self.editValue.setFixedSize(50,30)
        self.editValue.setText("0")
 
        self.slider.valueChanged.connect(self.syncValues)
        self.editValue.textChanged.connect(self.changedValue)

        sliderLayout.addWidget(self.editValue)
        sliderLayout.addWidget(self.slider)

        self.allButtons += [self.slider, self.editValue]

        self.brushLayout.addWidget(sliderGroup)

    def syncValues(self, size):
        """Syncs values of the slider and 
        brush size option from Paint Vertex 
        Color Tool from Maya
        """
        size = self.slider.value() / 100
        self.editValue.setText(str(size))
        cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e=True, radius = (size))

    def changedValue(self, text):
            """
            Changes text from editText to a float 
            and assigns it back to the slider
            """
            size = float(text)
            sliderValue = int(size * 100)
            self.slider.setValue(sliderValue) 

    def activateSymmetry(self):
        """Activates or deactivates symmetry 
        for a  paint brush by calling the symmetry
        option from original Paint Vertex Color brush
        """
        symmetryGroup = QtWidgets.QGroupBox()

        symmetryLayout = QtWidgets.QHBoxLayout()
        symmetryGroup.setLayout(symmetryLayout)

        symmetryButton = QtWidgets.QPushButton("Activate the symmetry")
        symmetryButton.clicked.connect(self.paintTab_instance.activateSymmetry)

        deSymmetryButton = QtWidgets.QPushButton("Deactivate the symmetry")
        deSymmetryButton.clicked.connect(self.paintTab_instance.deactivateSymmetry)

        symmetryCheckboxX = QCheckBox("X", self)
        symmetryCheckboxX.clicked.connect(lambda : self.paintTab_instance.symmetryAxis("x"))

        symmetryCheckboxY = QCheckBox("Y", self)
        symmetryCheckboxY.clicked.connect(lambda : self.paintTab_instance.symmetryAxis("y"))

        symmetryCheckboxZ = QCheckBox("Z", self)
        symmetryCheckboxZ.clicked.connect(lambda : self.paintTab_instance.symmetryAxis("z"))

        symmetryLayout.addWidget(symmetryButton)
        symmetryLayout.addWidget(deSymmetryButton)
        symmetryLayout.addWidget(symmetryCheckboxX)
        symmetryLayout.addWidget(symmetryCheckboxY)
        symmetryLayout.addWidget(symmetryCheckboxZ)

        self.allButtons += [symmetryButton, deSymmetryButton, symmetryCheckboxX, symmetryCheckboxY, symmetryCheckboxZ]

        self.brushLayout.addWidget(symmetryGroup)

    def templateTab(self):

        templateTabBody = QtWidgets.QWidget()
        self.tabMenu.addTab(templateTabBody, "Use reference template")

        self.templateLayout = QtWidgets.QGridLayout()
        templateTabBody.setLayout(self.templateLayout)

        self.templateText()
        self.templateImages()

    def templateText(self):

        templateTextGroup = QtWidgets.QGroupBox("Explanation")

        templateTextLayout = QtWidgets.QGridLayout()
        templateTextGroup.setLayout(templateTextLayout)
        templateTextGroup.setFixedHeight(200)

        text = QLabel("FOR FACES ONLY!")
                      
        text2 = QLabel("If you wish to use one of the provided templates please remember that it is only projecting on the front of the face "
                      "and might need some adjusting of the UVs inside the UV Editor with 'Adjust UVs size to the reference' button. "

                      "After reajusting, if you also wish to paint the sides simply click 'Paint' button. "
                      "When done, move onto QuadDraw tab.")
        
        text.setFont(QtGui.QFont("Sanserif", 10))
        text.setWordWrap(True)
        text.setAlignment(Qt.AlignCenter)
        text2.setFont(QtGui.QFont("Sanserif", 10))
        text2.setWordWrap(True)

        templateTextLayout.addWidget(text)
        templateTextLayout.addWidget(text2)

        self.templateLayout.addWidget(templateTextGroup)

    def templateImages(self):

        templateImagesGroup = QtWidgets.QGroupBox("Templates")

        templateImagesLayout = QtWidgets.QGridLayout()
        templateImagesGroup.setLayout(templateImagesLayout)
        templateImagesGroup.setFixedHeight(400)

        # First ref image
        image1 = QLabel(self)
        pixmap1 = QPixmap(self.relativePath('images/template1.jpeg'))
        scaledImage1 = pixmap1.scaledToHeight(200, Qt.SmoothTransformation)
        image1.setPixmap(scaledImage1)
        image1.resize(scaledImage1.width(), scaledImage1.height())

        # Button1
        useButton1 = QtWidgets.QPushButton("Use this")
        useButton1.setFixedSize(200, 50)
        useButton1.clicked.connect(lambda : self.templateTab_instance.shaderCreator("images/template1.jpeg"))
        useButton1.clicked.connect(self.hideFocusButton)

        # Second ref image
        image2 = QLabel(self)
        pixmap2 = QPixmap(self.relativePath('images/template2'))
        scaledImage2 = pixmap2.scaledToHeight(200, Qt.SmoothTransformation)
        image2.setPixmap(scaledImage2)
        image2.resize(scaledImage2.width(), scaledImage2.height())

        # Button2
        useButton2 = QtWidgets.QPushButton("Use this")
        useButton2.setFixedSize(200, 50)
        useButton2.clicked.connect(lambda : self.templateTab_instance.shaderCreator("images/template2.jpeg"))
        useButton2.clicked.connect(self.hideFocusButton)

        # Third ref image
        image3 = QLabel(self)
        pixmap3 = QPixmap(self.relativePath('images/template3.jpeg'))
        scaledImage3 = pixmap3.scaledToHeight(200, Qt.SmoothTransformation)
        image3.setPixmap(scaledImage3)
        image3.resize(scaledImage3.width(), scaledImage3.height())

        # Button3
        useButton3 = QtWidgets.QPushButton("Use this")
        useButton3.setFixedSize(200, 50)
        useButton3.clicked.connect(lambda : self.templateTab_instance.shaderCreator("images/template3.jpeg"))
        useButton3.clicked.connect(self.hideFocusButton)

        # Adjust button
        adjustButton = QtWidgets.QPushButton("Adjust UVs size to the reference")
        adjustButton.clicked.connect(lambda : self.templateTab_instance.adjustUVs())

        # Paint button
        paintButton = QtWidgets.QPushButton("Paint")
        paintButton.clicked.connect(self.templateTab_instance.selectObjectMode)
        paintButton.clicked.connect(self.unhidePaintTab)

        doneButton = QtWidgets.QPushButton("Done")
        doneButton.clicked.connect(lambda : self.templateTab_instance.doneTemplate())

        templateImagesLayout.addWidget(image1, 0, 0)
        templateImagesLayout.addWidget(useButton1, 1, 0)
        templateImagesLayout.addWidget(adjustButton, 2, 0)

        templateImagesLayout.addWidget(image2, 0, 1)
        templateImagesLayout.addWidget(useButton2, 1, 1)
        templateImagesLayout.addWidget(paintButton, 2, 1)

        templateImagesLayout.addWidget(image3, 0, 2)
        templateImagesLayout.addWidget(useButton3, 1, 2)
        templateImagesLayout.addWidget(doneButton, 2, 2)

        self.templateLayout.addWidget(templateImagesGroup)

        self.allButtons += [useButton1, useButton2, useButton3, adjustButton, paintButton, doneButton]

        
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

    def hideFocusButton(self):

        self.QuadFocusButton.hide()
        self.tabMenu.setTabEnabled(1, False)

    def unhidePaintTab(self):
        self.tabMenu.setTabEnabled(1, True)
        self.tabMenu.setCurrentIndex(1)

    def resetPaintTab(self):
        self.tabMenu.setTabEnabled(1, True)

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