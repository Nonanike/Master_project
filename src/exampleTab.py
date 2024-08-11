import maya.cmds as cmds
import os

class exampleTab():
    
    def createImagePlane(self, relPath):
        """ Creates an imagePlane in Maya with the corresponding file path"""
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(scriptDir, relPath)


        cmds.imagePlane(fileName=filePath)

            
    # def createImagePlane(self, filePath):
    #     """ Creates an imagePlane in Maya with the corresponding file path"""
    #     # scriptDir = os.path.dirname(os.path.abspath(__file__))
    #     # filePath = os.path.join(scriptDir, relPath)


    #     cmds.imagePlane(fileName=filePath)