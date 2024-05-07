### 2024 Alex Poulin
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QGraphicsView, QPushButton
import numpy as np

from commonWidgets import saveButtonCom, saveFileCom, errorDialogueCom, configureGraphCom, setupFigureCom

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DistCrve(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    #result = np.zeros((50,50))
    
    def __init__(self, results, tifArr, dat, type, posStart, posEnd, energiesLow, energiesHigh):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        #init variables
        self.result = results
        self.newResult = None
        self.energiesLow = energiesLow
        self.energiesHigh = energiesHigh
        self.type = type
        self.dat = dat
        #set up the box selection
        if (posStart[0] is None or posStart[1] is None or posEnd[0] is None or posEnd[1] is None):
            self.posStart = posStart
            self.posEnd = posEnd
        else:
            self.posStart = (posStart[0], self.remap(posStart[1], 
                                                     self.energiesLow, self.energiesHigh, 
                                                     0, self.result.shape[0]))
            self.posEnd = (posEnd[0], self.remap(posEnd[1], 
                                                 self.energiesLow, self.energiesHigh, 
                                                 0, self.result.shape[0]))
        #set up window
        self.setWindowTitle(type)
        self.layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol2 = QVBoxLayout()
        #set up the UI
        self.setupUI()
        #finalize layout
        self.layoutCol2.addWidget(self.canvas)
        self.layoutRow1.addLayout(self.layoutCol1)
        self.layoutRow1.addLayout(self.layoutCol2)
        self.setLayout(self.layoutRow1)
        
    def setupUI(self):
        #setup the save button
        saveButtonCom(self, "Save File")
        self.layoutCol1.addWidget(self.saveButton)
        
        #setupFigure
        setupFigureCom(self)
        
        #build
        self.show()
        self.buildDC()
        self.configureGraph()
        
    #remaps to the energy range
    def remap(self, value, start1, stop1, start2, stop2):
        # Scale input value from the original range to a value between 0 and 1
        normalized_value = (value - start1) / (stop1 - start1)
        # Scale the normalized value to the new range
        return start2 + normalized_value * (stop2 - start2)
        
    #builds the distribution curve
    def buildDC(self):
        self.ax = self.figure.add_subplot(111) #add subplot
        self.ax.clear() #clear any old ones
        self.newResult = self.configureType() #get data
        self.ax.plot(self.newResult[0], '-') #plot
        self.canvas.draw() #redraw
        
    #configures the graph 
    def configureGraph(self):
        configureGraphCom(self, self.type, 'Space', 'Intensity')
    
    #configures the type of distribution curve    
    def configureType(self):
        #get the points based on box selection
        if self.posStart[0] is None or self.posStart[1] is None or self.posEnd[0] is None or self.posEnd[1] is None: #get full image
            selectedBox = self.result
        else:
            selectedBox = self.result[int(min(self.posStart[1], self.posEnd[1])): int(max(self.posStart[1], self.posEnd[1])), 
                                      int(min(self.posStart[0], self.posEnd[0])): int(max(self.posStart[0], self.posEnd[0]))]
        #now integrate based on type
        if self.type == "EDC": #EDC integration over x
            newResult = np.zeros(shape = (1, selectedBox.shape[0]))
            for row in selectedBox:
                for col in range(len(newResult[0])):
                    newResult[0][col] += row[col]
                    
        else: #MDC integration over y
            newResult = np.zeros(shape = (1, selectedBox.shape[1]))
            for row in range(selectedBox.shape[0]): #range of result height
                newResult[0] += selectedBox[row]
                
        newResult = newResult.astype(float)
        return newResult
    
    #saves the file
    def saveFile(self):
        saveFileCom(self, self.newResult)
        
    #throws an error dialogue   
    def errorDialogue(self, title, message):
        errorDialogueCom(self, title, message)
        return False
        
         
        