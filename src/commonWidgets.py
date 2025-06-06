### 2024 Alex Poulin
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QPushButton, QDialogButtonBox, QVBoxLayout, QGroupBox, QLineEdit, QHBoxLayout, QCheckBox, QSizePolicy
from PyQt6.QtCore import QDir

import numpy as np
import os, sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from subprocess import check_call as run 
from getopt import getopt, GetoptError 

from src.widgets.QFileDialogFlatField import QFileDialogFlatFieldWidget
from src.widgets.plottoolbar import matplotToolbar

#remaps to the energy range
def remap(value, start1, stop1, start2, stop2):
    # Scale input value from the original range to a value between 0 and 1
    normalized_value = (value - start1) / (stop1 - start1)
    # Scale the normalized value to the new range
    return start2 + normalized_value * (stop2 - start2)

#rescales arrays
def rescale(original_array, new_min, new_max):
    # Scale the array to range from 0 to 1
    #resized_array = (original_array - original_array.min()) * (new_max - new_min) / (original_array.max() - original_array.min()) + new_min
    resized_array = np.interp(original_array, (original_array.min(), original_array.max()), (new_min, new_max))

    # Print the resized array
    # print(resized_array)
    return resized_array

def save_button_com(self, text):
    self.save_button = QPushButton(text)
    self.save_button.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
    self.save_button.clicked.connect(self.save_file)

def save_file_com(self, text):
    #options = QFileDialog.options()
    #options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getSaveFileName(self,"Save File","","Text Files(*.txt)")#,options = options)
    if file_name:
        f = open(file_name, 'w')
        # np.set_printoptions(threshold=np.inf)
        f.write(np.array_str(text))
        self.setWindowTitle(str(os.path.basename(file_name)) + " - ARPES Analysis")
        f.close()
        # np.set_printoptions()#revert todefautl
        return True
    else:
        return self.error_dialogue("Error", "File not saved")
        
def error_dialogue_com(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()
        return False

def configure_graph_com(self, type, x, y):
    self.ax.set_title(type)
    if type == "EDC" :
        y = "Energy"
        x = "Intensity"
    elif type == "MDC" :
        y = "Momentum"
        x = "Space"
    self.ax.set_xlabel(x)
    self.ax.set_ylabel(y)
    
    self.figure.tight_layout()
    #self.figure.patch.set_facecolor('white')
    #self.figure.patch.set_alpha(0)
    #self.canvas.setStyleSheet("background-color:transparent;")
    self.ax.spines["top"].set_color("white")
    self.ax.spines["bottom"].set_color("white")
    self.ax.spines["left"].set_color("white")
    self.ax.spines["right"].set_color("white")
    self.ax.tick_params(axis='x', colors='white')
    self.ax.tick_params(axis='y', colors='white')
    self.ax.yaxis.label.set_color('white')
    self.ax.xaxis.label.set_color('white')
    self.ax.title.set_color('white')
    self.ax.grid(True)
    #self.ax.invert_yaxis()
    self.canvas.draw()
    
def setup_figure_com(self):
    # a figure instance to plot on
    self.figure = Figure()
    # this is the Canvas Widget that displays the `figure`
    # it takes the `figure` instance as a parameter to __init__
    self.canvas = FigureCanvas(self.figure)
    # Create a Navigation Toolbar for zooming/panning
    #self.toolbar = NavigationToolbar(self.canvas, self)
    self.toolbar = matplotToolbar(self.canvas, self)
        
    # Add toolbar and canvas to the layout
    #self.layout.addWidget(self.toolbar)
    
    widthPixels = 2080
    heightPixels = 810
    dpi = self.figure.get_dpi()
    widthInches = widthPixels / dpi
    heightInches = heightPixels / dpi
    self.figure.set_size_inches(widthInches, heightInches)

    self.figure.patch.set_facecolor('white')
    self.figure.patch.set_alpha(0)
    #sest tight layout
    #self.figure.tight_layout()
    self.canvas.setStyleSheet("background-color:transparent;")
    self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    self.ax = self.figure.add_subplot(111)
    
def reset_button_com(self):
    # Create a square button
    self.resetButton = QPushButton("Reset Line")
    self.resetButton.setFixedSize(100, 25)  # Set the fixed size of the button to create a square shape
    self.resetButton.clicked.connect(self.reset_line)
    #self.resetButton.hide()
    self.resetButton.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")



##lowkey who knows if this update features works
RELEASE = 'master' # default release 
SRC_DIR = "$HOME/.src" # checkout directory 
UPDATE_CMD = ( # base command 
'pip install --src="%s" --upgrade -e ' 
'git://github.com/poulinal/ARPES.git@%s#egg=ARPES' 
)
#@command 
def update(args): 
    try: 
        opts, args = getopt(args, 'sr:', ['sudo', 'src=', 'release=', 'commit=']) 
    except GetoptError as err: 
        #log(err) 
        print(err)
        #usage(error_codes['option'])

    sudo = False 
    src_dir = SRC_DIR 
    release = RELEASE 
    commit = None 
    for opt, arg in opts: 
        if opt in ('-s', '--sudo'): 
            sudo = True 
        elif opt in ('-r', '--release'): 
            release = arg 
        elif opt in ('--src',): 
            src_dir = arg 
        elif opt in ('--commit',): 
            commit = arg

    if release[0].isdigit(): ## Check if it is a version 
        release = 'r' + release 
    release = 'origin/' + release ## assume it is a branch

    if commit is not None: ## if a commit is supplied use that 
        cmd = UPDATE_CMD % (src_dir, commit) 
    else: 
        cmd = UPDATE_CMD % (src_dir, release)

    if sudo: 
        run('sudo %s' % cmd) 
    else: 
        run(cmd)