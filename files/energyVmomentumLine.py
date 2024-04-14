### 2024 Alex Poulin

from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider
from PyQt6.QtWidgets import QRadioButton, QFileDialog, QCheckBox, QButtonGroup, QGraphicsView 
from PyQt6.QtWidgets import QLineEdit, QPushButton
from PyQt6.QtGui import QMouseEvent, QPixmap, QPainter, QPen, QColor, QIntValidator
from PyQt6.QtCore import Qt, QDir, QPoint, QTimer
from tifConv import tiffIm
from PIL import Image, ImageQt
import numpy as np
import os, sys

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class EnergyVMomentum(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    #result = np.zeros((50,50))
    
    def __init__(self, results):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        
        self.setWindowTitle("Energy vs Momentum Plot")

        self.layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol2 = QVBoxLayout()
        
        self.label = QLabel("Another Window")
        self.layoutCol1.addWidget(self.label)
        self.result = results
        self.xSliderValue = 0
        self.ySliderValue = 0
        self.SliderChosen = ""
        
        
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        
        self.show()
        self.ax = self.figure.add_subplot(111)
        self.buildEM()
        self.figure.tight_layout()
        
        self.labelX = QLineEdit()
        self.labelY = QLineEdit()
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 9)
        self.labelX.setValidator(onlyInt)
        self.labelX.setMaxLength(2)
        self.labelY.setValidator(onlyInt)
        self.labelY.setMaxLength(2)
        self.labelX.textEdited.connect(self.text_edited)
        self.labelY.textEdited.connect(self.text_edited)
        
        self.sliderX = QSlider(Qt.Orientation.Horizontal) #create new horizontal slider
        self.sliderY = QSlider(Qt.Orientation.Vertical) #create new horizontal slider
        self.sliderX.valueChanged.connect(self.slider_value_changed) #on change, call slider_value_changed
        self.sliderY.valueChanged.connect(self.slider_value_changed) #on change, call slider_value_changed
        
        self.layoutCol1.addWidget(self.sliderY, stretch=1)  # Add the slider to the layout with stretch=1 to make it take full width
        self.layoutCol1.addWidget(self.labelY)
        self.sliderX.setRange(0, int(self.result.shape[0]) - 1)  # Set the range of the slider to the width of the image
        self.sliderY.setRange(0, int(self.result.shape[1]) - 1)  # Set the range of the slider to the height of the image
        self.layoutCol2.addWidget(self.canvas)
        self.layoutCol2.addWidget(self.sliderX, stretch=1)
        self.layoutCol2.addWidget(self.labelX)
        self.layoutRow1.addLayout(self.layoutCol1)
        self.layoutRow1.addLayout(self.layoutCol2)
        #self.central_widget.setLayout(self.layoutRow1)
        self.setLayout(self.layoutRow1)
        
        
        # Setup a timer to trigger the redraw by calling update_plot.
        '''
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        '''
    
    def text_edited(self, s):
        if (self.textLineX.text() != "" and self.textLineY.text() != "" and self.textLineFinalX.text() != "" and self.textLineFinalY.text() != ""):
            pos = QPoint(int(self.textLineX.text()), int(self.textLineY.text()))
            self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
            self.makeLine(pos)
            
            
    def slider_value_changed(self, value):
        sender = self.sender()
        if sender == self.sliderX:
            self.xSliderValue = value
            self.SliderChosen = "x"
            self.labelX = QLabel(str(value))
            #print(self.xSliderValue, self.ySliderValue)
        elif sender == self.sliderY:
            self.ySliderValue = value
            self.SliderChosen = "y"
            #print(self.xSliderValue, self.ySliderValue)
            self.labelY = QLabel(str(value))
        self.buildEM()
        
    def buildEM(self):
        #this is for graph
        data = self.result
        
        # discards the old graph
        self.ax.clear()
        
        
        if self.SliderChosen != "":
            if self.SliderChosen == "x":
                dataX = np.linspace(self.xSliderValue, self.xSliderValue, data.shape[1])
                dataY = np.linspace(0, data.shape[1], data.shape[1])
            elif self.SliderChosen == "y":
                dataX = np.linspace(0, data.shape[0], data.shape[0])
                dataY = np.linspace(self.ySliderValue, self.ySliderValue, data.shape[0])
            #print(dataX, dataY)
            line2 = self.ax.plot(dataX, dataY, '-', color = "yellow")
            #print(self.ax.gcf().axes)
            #print(self.figure.axes.lines[1])
            self.canvas.draw()
        
        line1 = self.ax.imshow(data, cmap='gray')
        self.ax.set_xlabel('Momentum')
        self.ax.set_ylabel('Energy') #recipricsl dpsce #jahn-teller effect
        self.ax.invert_yaxis()
        #ax.set_title('Energy vs Momentum')
        self.ax.grid(True)

        # refresh canvas
        self.canvas.draw()
    
    def buildLine(self):
        data = self.result
        if self.SliderChosen != "":
            if self.SliderChosen == "x":
                dataX = np.linspace(self.xSliderValue, self.xSliderValue, data.shape[1])
                dataY = np.linspace(0, data.shape[1], data.shape[1])
            elif self.SliderChosen == "y":
                dataX = np.linspace(0, data.shape[0], data.shape[0])
                dataY = np.linspace(self.ySliderValue, self.ySliderValue, data.shape[0])
            #print(dataX, dataY)
            line2 = self.ax.plot(dataX, dataY, '-')
            print(self.ax.gcf().axes)
            #print(self.figure.axes.lines[1])
        self.canvas.draw()
        

        
''' 
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.
'''