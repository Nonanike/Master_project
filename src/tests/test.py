import unittest
from unittest.mock import patch
# import maya.standalone  # Needed for running Maya in batch mode
# maya.standalone.initialize(name='python')
import maya.cmds as cmds

from paintTab import PaintTab

# Test case for paint_tool class
class TestPaintTab(unittest.TestCase):
    
    def setUp(self):
        """Set up the environment before each test."""
        # You could create a new scene or set some initial state if needed
        cmds.file(new=True, force=True)

    @patch('maya.cmds.artAttrPaintVertexCtx')
    @patch('maya.cmds.currentCtx', return_value = 'currentContext')
    def test_paintTool_execution(self, mockCurrentCtx, mockArtAttrPaintVertexCtx):
        """Test if the paintTool method executes without errors."""
        tool = PaintTab()
        (R,G,B,A) = (0.0,0.0,0.0,0.0)

        try:
            tool.paintTool(R,G,B,A)

            # Assert
            mockCurrentCtx.assert_called_once()
            mockArtAttrPaintVertexCtx.assert_called_once_with('currentContext', e=True, colorRGBAValue = (R,G,B,A)) # If it runs without error, pass the test
            # If it runs without error, pass the test
        except Exception as e:
            self.fail(f"paintTool() raised an exception {e}")

    @patch('maya.cmds.setToolTo')
    def test_exitPaintTool_execution(self, mockSetToolTo):
        """Test if the exitPaintTool method executes without errors."""
        tool = PaintTab()
        try:
            tool.exitPaintTool()

            mockSetToolTo.assert_called_once_with('selectSuperContext')

            # self.assertTrue(True)  # If it runs without error, pass the test
        except Exception as e:
            self.fail(f"exitPaintTool() raised an exception {e}")
    
    @patch('maya.cmds.artAttrPaintVertexCtx')
    @patch('maya.cmds.currentCtx', return_value = 'currentContext')
    def test_activateSymmetry_execution(self,  mockCurrentCtx, mockArtAttrPaintVertexCtx):
        """Test if the activateSymmetry method executes without errors."""
        tool = PaintTab()

        try:
            tool.activateSymmetry()

            # Assert
            mockCurrentCtx.assert_called_once()
            mockArtAttrPaintVertexCtx.assert_called_once_with('currentContext', e=True, reflection=True) # If it runs without error, pass the test
        except Exception as e:
            self.fail(f"activateSymmetry() raised an exception {e}")

    @patch('maya.cmds.artAttrPaintVertexCtx')
    @patch('maya.cmds.currentCtx', return_value = 'currentContext')
    def test_deactivateSymmetry_execution(self,  mockCurrentCtx, mockArtAttrPaintVertexCtx):
        """Test if the deactivateSymmetry method executes without errors."""
        tool = PaintTab()

        try:
            tool.deactivateSymmetry()

            # Assert
            mockCurrentCtx.assert_called_once()
            mockArtAttrPaintVertexCtx.assert_called_once_with('currentContext', e=True, reflection=False) # If it runs without error, pass the test
        except Exception as e:
            self.fail(f"deactivateSymmetry() raised an exception {e}")

    @patch('maya.cmds.artAttrPaintVertexCtx')
    @patch('maya.cmds.currentCtx', return_value = 'currentContext')
    def symmetryAxis(self, mockCurrentCtx, mockArtAttrPaintVertexCtx):
        tool = PaintTab()
        axis = "x"

        try:
            tool.symmetryAxis(axis)

            # Assert
            mockCurrentCtx.assert_called_once()
            mockArtAttrPaintVertexCtx.assert_called_once_with('currentContext', e=True, ra=axis) # If it runs without error, pass the test
        except Exception as e:
            self.fail(f"symmetryAxis() raised an exception {e}")

    def tearDown(self):
        """Clean up the environment after each test."""
        # You could delete the scene or undo the changes made during the test
        cmds.file(new=True, force=True)  # Clean up by creating a new empty scene

if __name__ == '__main__':
    unittest.main()


    @patch('maya.cmds.select', retrun_value='pSphere1')
    @patch('maya.cmds.duplicate', retrun_name='duplicated')
    @patch('maya.cmds.createDisplayLayer', return_layer='display')
    @patch('maya.cmds. cmds.setAttr')
    def test_duplicatedMesh_execution(self, mockSelect, mockDuplicate, mockCreateDisplayLayer, mockSetAttr):
        """Test if the duplicatedMesh method executes without errors."""
        tool = quadDrawTab()
        result = tool.duplicateMesh()

        try:
            tool.duplicateMesh()

            # Assert
            self.assertEqual(result, 'duplicated')
            mockSelect.assert_called_once()
            mockDuplicate.assert_called_once()
            mockCreateDisplayLayer.assert_called_once()
            mockSetAttr.assert_called_once_with("display.visibility", 0)
            # If it runs without error, pass the test
        except Exception as e:
            self.fail(f"duplicatedMesh() raised an exception {e}")
