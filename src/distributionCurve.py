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
    
    def __init__(self, typePlot, curveResults, extentSpace = None):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        #init variables
        # self.result = results
        self.typePlot = typePlot
        self.curveResults = curveResults
        # print(f"curvereesults: {self.curveResults}, type: {type(self.curveResults)}")
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
        self.extentSpace = extentSpace
        print(f"DistCrve: extentSpace: {extentSpace}")
        
        #set up window
        self.setWindowTitle(self.typePlot)
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
        self.distrGraphFig = arpesGraph(graphtype="basic")
        x, y = zip(*self.getDistrData(self.gaussian))
        
        transformType = "None"
        if self.typePlot == "EDC":
            transformType = "y"
            self.distrGraphFig.setLabels(xlabel="Energy (eV)", ylabel="Intensity (a.u.)", title="Energy Distribution Curve (EDC)")
        elif self.typePlot == "MDC":
            transformType = "x"
            self.distrGraphFig.setLabels(xlabel="Pixels", ylabel="Intensity (a.u.)", title="Momentum Distribution Curve (MDC)")
            
        self.distrGraphFig.updateDCLine(x, y, colorline='blue', extentSpace=self.extentSpace, transform=transformType)
        self.layoutCol2.addWidget(self.distrGraphFig)
        
        #build
        # self.show()
        # self.build_DC()
        # self.configure_graph()
        

        
    #get data
    def getDistrData(self, gaussian = False):
        if gaussian:
            return gaussian_filter(self.curveResults, sigma=1.5)
        else:
            return self.curveResults
        
    ##TODO: check tuple compatibilty
    
         
        