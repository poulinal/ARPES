from PyQt6.QtWidgets import QFileDialog, QMessageBox, QPushButton

import numpy as np
import os, sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def saveButtonCom(self, text):
    self.saveButton = QPushButton(text)
    self.saveButton.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
    self.saveButton.clicked.connect(self.saveFile)

def saveFileCom(self, text):
    #options = QFileDialog.options()
    #options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getSaveFileName(self,"Save File","","Text Files(*.txt)")#,options = options)
    if file_name:
        f = open(file_name, 'w')
        np.set_printoptions(threshold=np.inf)
        f.write(np.array_str(text))
        self.setWindowTitle(str(os.path.basename(file_name)) + " - ARPES Analysis")
        f.close()
        np.set_printoptions()#revert to defautl
        return True
    else:
        return self.errorDialogue("Error", "File not saved")
        
def errorDialogueCom(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()
        return False

def configureGraphCom(self, type, x, y):
    self.ax.set_title(type)
    self.ax.set_xlabel(x)
    self.ax.set_ylabel(y)
    
    self.figure.tight_layout()
    self.figure.patch.set_facecolor('white')
    self.figure.patch.set_alpha(0)
    self.canvas.setStyleSheet("background-color:transparent;")
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
    
def setupFigureCom(self):
    # a figure instance to plot on
    self.figure = Figure()
    # this is the Canvas Widget that displays the `figure`
    # it takes the `figure` instance as a parameter to __init__
    self.canvas = FigureCanvas(self.figure)
    
def resetButtonCom(self):
    # Create a square button
    self.resetButton = QPushButton("Reset Line")
    self.resetButton.setFixedSize(75, 25)  # Set the fixed size of the button to create a square shape
    self.resetButton.clicked.connect(self.resetLine)
    self.resetButton.hide() == True