# A_Study_On_Binary_Image_Representations
A study of various transformations on compressed binary image representations

## Setup
An Anaconda setup in Linux is preferred, however a Windows setup would also do.

* Anaconda for Linux (Python 3.6)
https://docs.anaconda.com/anaconda/install/linux/

* Anaconda for Windows (Python 3.6):
https://www.anaconda.com/download/

Install external dependencies as:
```
pip install numpy Pillow opencv-python
```
## Algorithms and their usage
The following are the three areas that have been studied as a part of this work:
1. **Inter-conversion between run-forests and quadtrees:**
	* For run-forest to quadtree conversion, run
		```
		python run_forest_to_quadtree.py path_to_run_forest_file
		```
	* For quadtree to run-forest conversion, run
		```
		python quadtree_to_run_forest.py path_to_file_containing_quadtree_codes
		```
2. **Geometric transformations on run-forests** -  The following geometric transformations have been implemented:
	* Scaling
		* Subsampling
		* Zooming
	* Rotation - A single module contains two different functions for clockwise and anticlockwise rotations.
	* Translation - A single module contains two different functions for horizontal and vertical translations.
	The scripts can be run as:
		```
		python run_forest_geo_op path_to_run_forest_file
		```
		where geo_op is the name of the geometric operation which has to be performed.
		Eg:
		```
		python run_forest_translation.py img_run_forest.txt
		```
		The main functions implementing the geometric operations have the same names as the respective operations they implement and they take as arguments a run-forest and a factor, if the operation requires one.

3. **Morphological transformations on run-forests** -  The following morphological transformations have been implemented:
	* Erosion
	* Dilation
	* Hit-or-miss transform
	The scripts can be run as:
		```
		python run_forest_morph_op path_to_run_forest_file
		```
		where morph_op is the name of the morphological operation which has to be performed.
		Eg:
		```
		python run_forest_erosion.py img_run_forest.txt
		```
		The main functions implementing the morphological transformations have the same names as the respective transformations they implement and they take as arguments a run-forest and a structuring element, using which the run-forest is transformed.
		
