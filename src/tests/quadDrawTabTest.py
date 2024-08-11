import unittest
from unittest.mock import patch
# import maya.standalone  # Needed for running Maya in batch mode
# maya.standalone.initialize(name='python')
import maya.cmds as cmds

from quadDrawTab import quadDrawTab

# Test case for quadDrawTab class
class TestQuadDrawTab(unittest.TestCase):
    
    def setUp(self):
        """Set up the environment before each test."""
        # You could create a new scene or set some initial state if needed
        cmds.file(new=True, force=True)

    @patch('maya.cmds.select', retrun_value='pSphere1')
    @patch('maya.cmds.polyColorPerVertex')
    def test_saveMesh_execution(self, mockSelect, mockPolyColorPerVertex):
        """Test if the saveMesh method executes without errors."""
        tool = quadDrawTab()
        result = tool.saveMesh()

        try:
            tool.saveMesh()
            # assert return_value

            # Assert
            # self.assertEqual(result, 'pSphere1')
            # mockSelect.assert_called_once()
            mockSelect.assert_called_with('pSphere1')
            mockPolyColorPerVertex.assert_called_once_with(rgb=(0.4, 0.4, 0.4))
            # If it runs without error, pass the test
        except Exception as e:
            self.fail(f"saveMesh() raised an exception {e}")

    @patch('maya.cmds.select')
    @patch('maya.cmds.duplicate', retrun_value= 'duplicated')
    @patch('maya.cmds.createDisplayLayer')
    @patch('maya.cmds.setAttr')
    def test_duplicatedMesh_execution(self, mockSelect, mockDuplicate, mockCreateDisplayLayer, mockSetAttr):
        """Test if the duplicatedMesh method executes without errors."""
        tool = quadDrawTab()
        mesh_name='pCube1'
        layer1 = "display.displayType"
        layer2 = "display.visibility"
        result = tool.duplicateMesh()

        try:
            tool.duplicateMesh()

            # Assert
            self.assertEqual(result, 'duplicated')
            mockSelect.assert_any_call(mesh_name)
            mockDuplicate.assert_called_once_with(name='duplicated')
            mockSelect.assert_any_call(clear=True)
            mockSelect.assert_any_call(mesh_name)
            mockCreateDisplayLayer.assert_called_once(name='display')
            mockSetAttr.assert_any_call(layer1, 2)
            mockSetAttr.assert_any_call(layer2, 0)
            mockSelect.assert_any_call('duplicated')
            # self.assertEqual(result, 'duplicated')
            # If it runs without error, pass the test
        except Exception as e:
            self.fail(f"duplicatedMesh() raised an exception {e}")

    def tearDown(self):
        """Clean up the environment after each test."""
        # You could delete the scene or undo the changes made during the test
        cmds.file(new=True, force=True)  # Clean up by creating a new empty scene

if __name__ == '__main__':
    unittest.main()