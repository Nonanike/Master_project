import unittest
from unittest.mock import patch
# import maya.standalone  # Needed for running Maya in batch mode
# maya.standalone.initialize(name='python')
import maya.cmds as cmds

from templateTab import useTemplate

# # Test case for paint_tool class
# class TestPaintTab(unittest.TestCase):
    
#     def setUp(self):
#         """Set up the environment before each test."""
#         # You could create a new scene or set some initial state if needed
#         cmds.file(new=True, force=True)

    # # @patch('maya.cmds.artAttrPaintVertexCtx')
    # # @patch('maya.cmds.currentCtx', return_value = 'currentContext')
    # def test_shaderCreator_execution(self):
    #     """Test if the shaderCreator method executes without errors."""
    #     tool = useTemplate()
    #     filePath = '/home/s5325378/Desktop/masters_project/images/hand_stylised.jpeg'
    #     try:
    #         tool.shaderCreator(filePath)

    #         # Assert
    #         mockImagePlane.assert_called_once_with(fileName=filePath) # If it runs without error, pass the test
    #     except Exception as e:
    #         self.fail(f"createImagePlane() raised an exception {e}")

    # @patch('maya.cmds.setToolTo')

    # @patch('maya.cmds.select')
    # @patch('maya.cmds.hilite')
    # def test_UVsCreator_execution(self, mockSetToolTo):
    #     """Test if the UVsCreator method executes without errors."""
    #     tool = useTemplate()
    #     mesh_name ='pSphere1'
    #     try:
    #         tool.UVsCreator()

    #         mockSetToolTo.assert_called_once_with('selectSuperContext')

    #         # self.assertTrue(True)  # If it runs without error, pass the test
    #     except Exception as e:
    #         self.fail(f"UVsCreator() raised an exception {e}")
    

    # def tearDown(self):
    #     """Clean up the environment after each test."""
    #     # You could delete the scene or undo the changes made during the test
    #     cmds.file(new=True, force=True)  # Clean up by creating a new empty scene

if __name__ == '__main__':
    unittest.main()