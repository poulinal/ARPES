### 2024 Alex Poulin
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QGraphicsView, QPushButton
import numpy as np
from scipy.ndimage import gaussian_filter

from src.commonWidgets import save_button_com, save_file_com, error_dialogue_com
from src.commonWidgets import configure_graph_com, setup_figure_com, remap, rescale

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from src.widgets.arpesGraph import arpesGraph


class DistCrve(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    #result = np.zeros((50,50))
    
    def __init__(self, type, curveResults):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        #init variables
        # self.result = results
        self.type = type
        self.curveResults = curveResults
        print(f"curvereesults: {self.curveResults}, type: {type(self.curveResults)}")
        self.gaussian = False
        # self.energiesLow = energiesLow
        # self.energiesHigh = energiesHigh
        # self.posStart = posStart
        # self.posEnd = posEnd
        #set up the box selection
        # if (self.posStart[0] is None or self.posStart[1] is None or self.posEnd[0] is None or self.posEnd[1] is None):
        #     self.datPosStart = self.posStart
        #     self.datPosEnd = self.posEnd
        # else:
        #     self.datPosStart = (self.posStart[0], remap(self.posStart[1], 
        #                                         self.energiesLow, self.energiesHigh, 
        #                                         0, self.result.shape[0]))
        #     self.datPosEnd = (self.posEnd[0], remap(self.posEnd[1], 
        #                                     self.energiesLow, self.energiesHigh, 
        #                                     0, self.result.shape[0]))
        #set up window
        self.setWindowTitle(type)
        self.layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol2 = QVBoxLayout()
        #set up the UI
        self.setup_UI()
        #finalize layout
        self.layoutRow1.addLayout(self.layoutCol1)
        self.layoutRow1.addLayout(self.layoutCol2)
        self.setLayout(self.layoutRow1)
        
    def setup_UI(self):
        #setup the save button
        # save_button_com(self, "Save File")
        # self.layoutCol1.addWidget(self.save_button)
        
        #setupFigure
        # setup_figure_com(self)
        self.distrGraphFig = arpesGraph()
        self.distrGraphFig.update_line(*self.getDistrData(self.gaussian), colorline='blue')
        self.layoutCol2.addWidget(self.distrGraphFig)
        
        #build
        # self.show()
        # self.build_DC()
        # self.configure_graph()
        
    #configures the graph 
    # def configure_graph(self):
    #     configure_graph_com(self, self.type, 'Intensity', '')
        
    #get data
    def getDistrData(self, gaussian = False):
        if gaussian:
            return gaussian_filter(self.curveResults, sigma=1.5)
        else:
            return self.curveResults
    
    #configures the type of distribution curve    
    # def configure_type(self):
    #     #get the points based on box selection
    #     if self.datPosStart[0] is None or self.datPosStart[1] is None or self.datPosEnd[0] is None or self.datPosEnd[1] is None: #get full image
    #         selectedBox = self.result
    #     else:
    #         selectedBox = self.result[int(min(self.datPosStart[1], self.datPosEnd[1])): int(max(self.datPosStart[1], self.datPosEnd[1])), 
    #                                   int(min(self.datPosStart[0], self.datPosEnd[0])): int(max(self.datPosStart[0], self.datPosEnd[0]))]
    #     #print(f"selectedBox: {selectedBox}")
    #     #now integrate based on type
    #     if self.type == "EDC": #EDC integration over x
    #         newResult = np.zeros(shape = (1, selectedBox.shape[0]))
    #         for row in selectedBox:
    #             for col in range(len(newResult[0])):
    #                 newResult[0][col] += row[col]
                    
    #     else: #MDC integration over y
    #         newResult = np.zeros(shape = (1, selectedBox.shape[1]))
    #         for row in range(selectedBox.shape[0]): #range of result height
    #             newResult[0] += selectedBox[row]
                
    #     newResult = newResult.astype(float)
    #     return newResult
    
    #saves the file
    # def save_file(self):
    #     save_file_com(self, self.newResult)
        
    # #throws an error dialogue   
    # def error_dialogue(self, title, message):
    #     error_dialogue_com(self, title, message)
    #     return False
        
         
        