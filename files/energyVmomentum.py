### 2024 Alex Poulin
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QGraphicsView, QPushButton
import numpy as np

from distributionCurve import DistCrve
from tifConv import getEnergies
from commonWidgets import saveButtonCom, saveFileCom, errorDialogueCom, configureGraphCom, setupFigureCom, resetButtonCom


"""
This "window" is a QWidget. If it has no parent, it
will appear as a free-floating window as we want.
"""
class EnergyVMomentum(QWidget):
    def __init__(self, results, path, tifArr, dat, info):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        #setup variables
        self.result = results
        self.startx = None
        self.starty = None
        self.lastx = None
        self.lasty = None
        self.tracking = False
        self.path = path
        self.tifArr = tifArr
        self.dat = dat
        self.info = info
        self.energiesLow = None
        self.energiesHigh = None
        
        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self._plot_ref = [None, None, None, None]
        
        #setup window
        self.setWindowTitle("Energy vs Momentum Plot")
        self.layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol2 = QVBoxLayout()
        self.label = QLabel("Another Window")
        self.layoutCol1.addWidget(self.label)
        #setupUI
        self.setupUI()
        #finialize layout
        self.layoutCol2.addWidget(self.canvas)
        self.layoutRow1.addLayout(self.layoutCol1)
        self.layoutRow1.addLayout(self.layoutCol2)
        self.setLayout(self.layoutRow1)
        
    def setupUI(self):
        saveButtonCom(self, "Save File")
        self.layoutCol1.addWidget(self.saveButton)
        
        self.intXButton = QPushButton("Int over X")
        self.intXButton.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
        self.layoutCol1.addWidget(self.intXButton)
        self.intYButton = QPushButton("Int over Y")
        self.intYButton.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
        self.layoutCol1.addWidget(self.intYButton)
        
        self.intXButton.clicked.connect(self.integrate)
        self.intYButton.clicked.connect(self.integrate)
        self.saveButton.clicked.connect(self.saveFile)
        
        #setupFigure
        setupFigureCom(self)
        
        # Connect the mouse events
        self.canvas.mpl_connect('button_press_event', self.plotMouseClick)
        self.canvas.mpl_connect('motion_notify_event', self.plotMouseMove)
        self.canvas.mpl_connect('button_release_event', self.plotMouseRelease)
        
        self.show()
        self.buildEM()
        
        #setup reset button
        resetButtonCom(self)
        self.layoutCol2.addWidget(self.resetButton)
    
    #resets the line
    def resetLine(self):
        self.buildEM()
        self.resetButton.hide()
        self.update()
        
    #start point on click
    def plotMouseClick(self, e):
        self.resetButton.show()
        self.tracking = not self.tracking
        if e.inaxes:
            self.startx = e.xdata
            self.starty = e.ydata
            
    #allow drag
    def plotMouseMove(self, e):
        #note the xdata gets the position in the graph --good for matplotlib
        #note the x gets the position in pixels from left and bottom of axes --good for pyqt
        if e.inaxes and self.tracking:
            pos = (e.xdata, e.ydata)
            self.lastx = e.xdata
            self.lasty = e.ydata
            self.createArea(pos)
    
    #release stop tracking
    def plotMouseRelease(self, e):
        self.tracking = False
        
    #build EM plot
    def buildEM(self):
        self.ax = self.figure.add_subplot(111)
        self.ax.clear() # discards the old graph
        #get data
        energies = getEnergies(self.path, self.dat)
        #set range and plot
        self.energiesLow = energies[0]
        self.energiesHigh = energies[len(energies)-1]
        self.ax.imshow(self.result, cmap='gray', extent=[0, self.result.shape[1], 
                                                         self.energiesLow, self.energiesHigh])
        #remap to the energies of the experiment
        self.ax.set_aspect(self.result.shape[1] / (energies[len(energies)-1] - energies[0]))
        # refresh canvas
        self.configureGraph()
        self.canvas.draw()
    
    #create the boxed area
    def createArea(self, pos):
        x0 = self.startx
        y0 = self.starty
        xf = pos[0]
        yf = pos[1]
        xLength = abs(x0 - xf)
        yLength = abs(y0 - yf)
        dataTopX = np.linspace(x0, xf, int(xLength))
        dataTopY = np.linspace(y0, y0, int(xLength))
        dataBottomX = np.linspace(x0, xf, int(xLength))
        dataBottomY = np.linspace(yf, yf, int(xLength))
        dataLeftX = np.linspace(x0, x0, int(xLength))
        dataLeftY = np.linspace(y0, yf, int(xLength))
        dataRightX = np.linspace(xf, xf, int(xLength))
        dataRightY = np.linspace(y0, yf, int(xLength))
        
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
            plot_refs = self.ax.plot(dataTopX, dataTopY, '-', color='yellow')
            self._plot_ref[0] = plot_refs[0]
            plot_refs = self.ax.plot(dataBottomX, dataBottomY, '-', color='yellow')
            self._plot_ref[1] = plot_refs[0]
            plot_refs = self.ax.plot(dataLeftX, dataLeftY, '-', color='yellow')
            self._plot_ref[2] = plot_refs[0]
            plot_refs = self.ax.plot(dataRightX, dataRightY, '-', color='yellow')
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
        self.canvas.draw()
    
    #configure the graph
    def configureGraph(self):
        configureGraphCom(self, 'Energy vs Momentum', 'Momentum', 'Energy')
        
    #integrate over x or y
    def integrate(self):
        if self.sender() == self.intXButton:
            type = "EDC"
        else:
            type = "MDC"
        #create new window
        self.w = DistCrve(self.result, self.tifArr, self.dat, type, (self.startx, self.starty), 
                          (self.lastx, self.lasty), self.energiesLow, self.energiesHigh)
        self.w.show()
         
    #save the file
    def saveFile(self):
        saveFileCom(self, self.result)
    
    #throws error dialogue 
    def errorDialogue(self, title, message):
        errorDialogueCom(self, title, message)
        return False
         
        