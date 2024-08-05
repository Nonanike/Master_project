import maya.cmds as cmds


class exampleTab():
    
    def createImagePlane(self, filePath):

        cmds.imagePlane(fileName=filePath)