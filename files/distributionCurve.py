### 2024 Alex Poulin

from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider
from PyQt6.QtWidgets import QCheckBox, QButtonGroup, QGraphicsView, QLineEdit, QPushButton
from PyQt6.QtCore import Qt, QDir, QPoint
from PIL import Image, ImageQt
import numpy as np
import os, sys

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class DistCrve(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    #result = np.zeros((50,50))
    
    def __init__(self, results, tifArr, dat, type):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        #self.setMouseTracking(True)
        
        self.setWindowTitle(type)

        self.layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol2 = QVBoxLayout()
        
        #self.label = QLabel("Another Window")
        #self.layoutCol1.addWidget(self.label)
        self.result = results
        self.startx = 0
        self.starty = 0
        self.tracking = False
        self.tifArr = tifArr
        self.type = type
        self.dat = dat
        
        #print(f"DC result: {self.result}")
        
        # Create a square button
        self.intXButton = QPushButton("Int over X")
        self.intXButton.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
        #self.layoutCol1.addWidget(self.intXButton)
        self.intYButton = QPushButton("Int over Y")
        self.intYButton.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
        #self.layoutCol1.addWidget(self.intYButton)
        
        
        # a figure instance to plot on
        self.figure = Figure()
        

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        
        self.show()
        self.buildEM()
        
        self.configureGraph()
        
        self.layoutCol2.addWidget(self.canvas)
        self.layoutRow1.addLayout(self.layoutCol1)
        self.layoutRow1.addLayout(self.layoutCol2)
        #self.central_widget.setLayout(self.layoutRow1)
        self.setLayout(self.layoutRow1)
        
        self.configureType()
        
        
    def buildEM(self):
        #this is for graph
        self.ax = self.figure.add_subplot(111)
        # discards the old graph
        self.ax.clear()
        

        #data = self.result
        #print(f"energies: {energies}")
        #print(f"len: {len(energies)}")
        #print(f"datashape: {data.shape}")
        #data[0] = energies
        #print(f"result: {self.result}")
        
        #aspectRatio = (energies[len(energies)-1] - energies[0]) / self.result.shape[0]
        #print(energies[0])
        #print(energies[len(energies)-1])
        #print(self.result.shape[0])
        #print(self.result.shape[1])
        #print((energies[len(energies)-1] - energies[0]))

        newResult = self.configureType()
        self.ax.plot(newResult[0], '-')
        '''
        for row in newResult[0]:
            print(row)
            self.ax.plot(row, '-')
            '''
        #self.ax.imshow(self.result, cmap='gray', extent=[0, self.result.shape[0], energies[0], energies[len(energies)-1]]) #recipricsl dpsce #jahn-teller effect
        #self.ax.set_aspect(self.result.shape[0] / (energies[len(energies)-1] - energies[0]))
        #self.ax.pcolormesh(np.linspace(0, self.result.shape[0], self.result.shape[0]), energies, self.result, cmap='gray', shading='nearest')

        # refresh canvas
        self.canvas.draw()
        
        
    def configureGraph(self):
        self.ax.set_title(self.type)
        self.ax.set_xlabel('Space')
        self.ax.set_ylabel('Intensity')
        
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
        
    def configureType(self):
        #only return those points in the array which align with x_new and y_new
        #print(f"resultshape: {result.shape}")
        if self.type == "MDC": #MDC integration over y
            newResult = np.zeros(shape = (1, self.result.shape[0]))
            #print(f"newResult: {newResult.shape}")
            for row in self.result:
                #print(f"row: {row}")
                #print(range(len(newResult[0])))
                for col in range(len(newResult[0])):
                    #print(row[col])
                    newResult[0][col] += row[col]
                    #print(f"newResult: {newResult}")
        else: #EDC integration over x
            newResult = np.zeros(shape = (1, self.result.shape[1]))
            #print(f"newResult: {newResult.shape}")
            for row in range(self.result.shape[0]): #range of result height
                for col in range(len(newResult)):
                    newResult[0] += self.result[row]
        #print(f"newResult: {newResult}")
        newResult = newResult.astype(float)
        return newResult
            
        
         
        