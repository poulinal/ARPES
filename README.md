This is some prelimnary code to visualize ARPES data curtosy of DeLTA Lab and NanoESCA Labs at NEU.
Mucho work in progress



Dependancies:
'''pip install pyqt6'''
'''pip install pillow'''
'''pip install matplotlib'''
'''pip install numpy'''
'''pip install scipy'''
'''pip install pandas'''


Note expected updates are shown here: 
https://unleashed-ferret-f75.notion.site/cf8bb74aa9094069be2738f1d213716c?v=52b7674c89cf4d59bbe272ea2d87a0b6&pvs=4

**To install:**
Simply to get the most recent main update do:
'''git clone https://github.com/poulinal/ARPES.git'''
This will clone this repository in the current directory. At any point, make sure to '''git pull''' to make sure you have the latest updates. 
Currently this program will be running on 'main.py' but eventually I want to release a single executable app instead. This app will also hopefully contain the ability to 

This repository is meant as an accumulation of code to assist in the data acquisition and analysis at DeLTA and NanoESCA labratories.
This repository is mostly written in python and pyqt. There is currently three main projects (two of which are planning a preliminary release soon)
all of which will be compiled into one program (however as these projects get bigger, this may end up switching into three separate programs):

**1) ARPES analysis**
This code works on datasets retrieved from NanoESCA's ARPES system. These datasets include a .dat file which holds the metadata for the experiment and .tif's which are the actual data. 
The program allows the user to scan through the different energies of the .tif's with some options to alter the image (i.e. contrast, colormap, etc.)
Additionally, a user can click on the image (a matplotlib imshow) and drag which constructs a line across the plot. 
By submitting this line, this creates a 'cut across the energies'. So the new image constructed has the x axis along the line, where the y axis goes through across all energies (an energy vs. momentum plot). From here the user can either save, or can once again click and drag, now creating a box starting from the left corner. The user can now integrate over x or y resulting in an energy distribution curve or momentum distribution curve, respectively. A plot is shown of this curve and once again the user has the ability to save the plot data. Further functionalities may be added in the future...


**2) XPS analysis**
This code works on datasets retrieved from NanoESCA's XPS system. These data include a .dat file which holds the metadata for the experiment and .tif's which are the actual data. The xps program upon opening this directory will integrate over the entire image to capture the intensity of electrons for that energy. This is repeated along every energy and a plot is created of this curve. This data can be saved as an .xlsx file.



**3) RIXS gui**
This code is very preliminary. But the premise is to have two types, one that is an html-python-flask system, another that is pyqt. This code will then allow a user to input various parameters of the RIXS program and show the output. Normally users would have to manually hard code this data and so this program will make this process much simpler and user friendly.



**To Run**
To run, make you way to the respository directory which should have a main.py in the home folder.
then do '''./main.py'''
Eventually I will build an executable that can simply be double tapped (and eventually automatically update).




**Other notes**
some dependencies this repository relies on:
numpy
matplotlib
pillow
pandas
