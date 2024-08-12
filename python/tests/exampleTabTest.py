import unittest
from unittest.mock import patch
# import maya.standalone  # Needed for running Maya in batch mode
# maya.standalone.initialize(name='python')
import maya.cmds as cmds

from exampleTab import exampleTab

# Test case for example class
class TestExampleTab(unittest.TestCase):
    
    def setUp(self):
        """Set up the environment before each test."""
        # You could create a new scene or set some initial state if needed
        cmds.file(new=True, force=True)

    @patch('maya.cmds.imagePlane')
    def test_createImagePlane_execution(self, mockImagePlane):
        """Test if the createImagePlane method executes without errors."""
        tool = exampleTab()
        filePath = '/home/s5325378/Desktop/masters_project/images/hand_stylised.jpeg'
        try:
            tool.createImagePlane(filePath)

            # Assert
            mockImagePlane.assert_called_once_with(fileName=filePath) # If it runs without error, pass the test
        except Exception as e:
            self.fail(f"createImagePlane() raised an exception {e}")

    def tearDown(self):
        """Clean up the environment after each test."""
        # You could delete the scene or undo the changes made during the test
        cmds.file(new=True, force=True)  # Clean up by creating a new empty scene

if __name__ == '__main__':
    unittest.main()