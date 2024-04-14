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
        #self.setMouseTracking(True)
        
        self.setWindowTitle("Energy vs Momentum Plot")

        self.layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol2 = QVBoxLayout()
        
        self.label = QLabel("Another Window")
        self.layoutCol1.addWidget(self.label)
        self.result = results
        self.startx = 0
        self.starty = 0
        self.last_x, self.last_y = None, None
        self.tracking = False
        
        
        # a figure instance to plot on
        self.figure = Figure()
        

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        
        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self._plot_ref = [None, None, None, None]
        
        # Connect the mouse click event
        self.canvas.mpl_connect('button_press_event', self.plotMouseClick)
        # Connect the mouse move event
        self.canvas.mpl_connect('motion_notify_event', self.plotMouseMove)
        self.canvas.mpl_connect('button_release_event', self.plotMouseRelease)
        
        self.show()
        self.buildEM()
        
        self.configureGraph()
        
        self.layoutCol2.addWidget(self.canvas)
        self.layoutRow1.addLayout(self.layoutCol1)
        self.layoutRow1.addLayout(self.layoutCol2)
        #self.central_widget.setLayout(self.layoutRow1)
        self.setLayout(self.layoutRow1)
        
    def plotMouseClick(self, e):
        #print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #   ('double' if e.dblclick else 'single', e.button,
        #    e.x, e.y, e.xdata, e.ydata))
        self.tracking = not self.tracking
        if e.inaxes:
            pos = QPoint(int(e.xdata),int(e.ydata))
            self.startx = pos.x()# - self.canvas.x()
            self.starty = pos.y()# - self.canvas.y()
            
    #allow drag
    def plotMouseMove(self, e):
        #note the xdata gets the position in the graph --good for matplotlib
        #note the x gets the position in pixels from left and bottom of axes --good for pyqt
        if e.inaxes and self.tracking:
            #print(f"Mouse position (x, y): ({e.x}, {e.y}), ({e.xdata}, {e.ydata})")
            #print(e.pos().x() - self.image_label.x()) //this is the true position with respect to the picture
            pos = QPoint(int(e.xdata), int(e.ydata))
            if self.last_x is None: # First event.
                #print("no last_x")
                self.last_x = pos.x()
                self.last_y = pos.y()
                return # Ignore the first time.
            
            self.createArea(pos)
            
    def plotMouseRelease(self, e):
        self.tracking = False
        
        
    def buildEM(self):
        #this is for graph
        self.ax = self.figure.add_subplot(111)
        # discards the old graph
        self.ax.clear()

        self.ax.imshow(self.result, cmap='gray') #recipricsl dpsce #jahn-teller effect
        self.ax.invert_yaxis()

        # refresh canvas
        self.canvas.draw()
        
    def createArea(self, pos):
        x0 = self.startx# - self.canvas.x()
        y0 = self.starty# - self.canvas.y()
        xf = pos.x()# - self.canvas.x()
        yf = pos.y()# - self.canvas.y()
        #print(x0, y0, xf, yf)
        #self.ax.clear()
        xLength = abs(x0 - xf)
        yLength = abs(y0 - yf)
        dataTopX = np.linspace(x0, xf, xLength)
        dataTopY = np.linspace(y0, y0, xLength)
        dataBottomX = np.linspace(x0, xf, xLength)
        dataBottomY = np.linspace(yf, yf, xLength)
        dataLeftX = np.linspace(x0, x0, yLength)
        dataLeftY = np.linspace(y0, yf, yLength)
        dataRightX = np.linspace(xf, xf, yLength)
        dataRightY = np.linspace(y0, yf, yLength)
        
        '''
        lineTop = self.ax.plot(dataTopX, dataTopY, '-')
        lineBottom = self.ax.plot(dataBottomX, dataBottomY, '-')
        lineLeft = self.ax.plot(dataLeftX, dataLeftY, '-')
        lineRight = self.ax.plot(dataRightX, dataRightY, '-')
        self.ax.clear()
        self.buildEM() 
        #this is clear and redrawing -- very laggy
        '''
        # Note: With this reference below, we no longer need to clear the axis.
        #Note: this takes more to store the references, but it is faster
        if self._plot_ref[0] is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.ax.plot(dataTopX, dataTopY, '-')
            self._plot_ref[0] = plot_refs[0]
            plot_refs = self.ax.plot(dataBottomX, dataBottomY, '-')
            self._plot_ref[1] = plot_refs[0]
            plot_refs = self.ax.plot(dataLeftX, dataLeftY, '-')
            self._plot_ref[2] = plot_refs[0]
            plot_refs = self.ax.plot(dataRightX, dataRightY, '-')
            self._plot_ref[3] = plot_refs[0]
            
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref[0].set_ydata(dataTopY)
            self._plot_ref[0].set_xdata(dataTopX)
            self._plot_ref[1].set_ydata(dataBottomY)
            self._plot_ref[1].set_xdata(dataBottomX)
            self._plot_ref[2].set_ydata(dataLeftY)
            self._plot_ref[2].set_xdata(dataLeftX)
            self._plot_ref[3].set_ydata(dataRightY)
            self._plot_ref[3].set_xdata(dataRightX)
        #self.ax.set_xlim(0, self.result.shape[0])
        #self.ax.set_ylim(0, self.result.shape[1])
        #self.ax.autoscale(enable=False)
        self.canvas.draw()
        
    def configureGraph(self):
        self.ax.set_title('Energy vs Momentum')
        self.ax.set_xlabel('Momentum')
        self.ax.set_ylabel('Energy')
        
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
        

         
        