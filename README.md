## Nina Kokot

# Maya Paint and Retopology pipeline tool

## Overview

This is a plug-in tool for Maya Autodesk that allows the user to learn the re-topology process and helps to improve the topology flow and saves time in the production pipeline.

## Requirements
* Maya Autodesk >= 2023
* Python >= 3.9
* Pyside2

## Installation
1. Download the project ZIP file from the GitHub with the green button that can be found above the the list 'Code' or clone the repository with 

   ```
   git clone git@github.com:Nonanike/Master_project.git
   ```

2. Navigate to this folder in the terminal and make sure you are inside it before running:
   ```
   python install.py
	```
3. Open Maya and int the top sheleves part find 'PaintAndRetopologyTool', then click on it to run it. If it is not showing, please restart Maya and try again.

## User instructions

1. First, select a mesh that will undergo the process of re-topology and press 'Select Mesh' button.

2. Look at the examples of different topologies provided in the 'Examples tab' and create any image planes as references if needed.

3. To paint references on the model:

	* Open 'Paint tab' and select the desired color and start painting on the mesh. 
	
	* To change a size simply look at the slider.

	* When done, exit the Paint tool with 'Exit the Paint Tool' button.

4. To use reference templates:

	* Open 'Use reference template' and read the explanation because this feautre is only for faces.

	* Choose the preferred template and click 'Use this'.

	* To reajust the UVs size, click button with a corresponding name and then press 'R' on the keyboard.

	* If there is a need for adding more paint on the other parts of the mesh, click 'Paint' button.

	* When done, exit the tool with 'Done'

5. To use QuadDraw tool:

	* Open 'QuadDraw tab' and activate it with 'START' button 

	* Start placing vertices directly onto the mesh, when there is four click SHIFT + LEFT MOUSE to create a new polygon

	* To focus on only one color at the time, click a button with the same name and pick the corresponding color from your model

	* When done, click 'DONE' to exit the tool and delete all the unecessary copies of the mesh

	* If both sides of the mesh can be the same, please use 'Mirror' button to mirror it

6. To start working on a new geometry, click 'Choose a New Mesh' and the tool will reset

## Testing
There are tests inside 'src/tests' folder. In order to run tests paste each of them straight into Maya's script editor and run it.

### Project structure

	/project
		/installScripts
		/plugins
			/paintRetoToolPlugin.py
		/src
			/images
			/tests
			/exampleTab.py
			/paintRetoTool.py
			/paintTab.py
			/quadDrawTab.py
			/templateTab.py
