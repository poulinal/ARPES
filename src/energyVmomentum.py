### 2024 Alex Poulin
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QGraphicsView, QPushButton
import numpy as np

from src.distributionCurve import DistCrve
from src.tifConv import get_energies
from src.commonWidgets import save_button_com, save_file_com, error_dialogue_com, configure_graph_com, setup_figure_com, reset_button_com

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
"""
This "window" is a QWidget. If it has no parent, it
will appear as a free-floating window as we want.
"""
class EnergyVMomentum(QWidget):
    def __init__(self, results, path, tifArr, dat):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        #setup variables
        self.result = results
        self.startx = None
        self.starty = None
        self.lastx = None
        self.lasty = None
        self.datax = None
        self.datay = None
        self.dataLastx = None
        self.dataLasty = None
        self.tracking = False
        self.path = path
        self.tifArr = tifArr
        self.dat = dat
        #self.info = info
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
        #setup_UI
        self.setup_UI()
        #finialize layout
        self.layoutCol2.addWidget(self.canvas)
        self.layoutRow1.addLayout(self.layoutCol1)
        self.layoutRow1.addLayout(self.layoutCol2)
        self.setLayout(self.layoutRow1)
        
    def setup_UI(self):
        save_button_com(self, "Save File")
        self.layoutCol1.addWidget(self.save_button)
        
        self.intXButton = QPushButton("Int over X")
        self.intXButton.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
        self.layoutCol1.addWidget(self.intXButton)
        self.intYButton = QPushButton("Int over Y")
        self.intYButton.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
        self.layoutCol1.addWidget(self.intYButton)
        
        self.intXButton.clicked.connect(self.integrate)
        self.intYButton.clicked.connect(self.integrate)
        self.save_button.clicked.connect(self.save_file)
        
        #setupFigure
        setup_figure_com(self)
        
        # Connect the mouse events
        self.canvas.mpl_connect('button_press_event', self.plot_mouse_click)
        self.canvas.mpl_connect('motion_notify_event', self.plot_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.plot_mouse_release)
        
        self.show()
        #self.ax = self.figure.add_subplot(111)
        self.build_EM()
        
        #setup reset button
        reset_button_com(self)
        self.layoutCol1.addWidget(self.resetButton)
    
    #resets the line
    def reset_line(self):
        #self.figure = Figure()
        #self.canvas = FigureCanvas(self.figure)
        #self.figure.clf()
        self.ax.cla()
        self._plot_ref[0] = None
        self.build_EM()
        self.resetButton.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")
        #self.resetButton.hide()
        #self.update()
        
    #start point on click
    def plot_mouse_click(self, e):
        #self.resetButton.show()
        self.resetButton.setStyleSheet("")
        self.tracking = not self.tracking
        if e.inaxes:
            self.startx = e.xdata
            self.starty = e.ydata
            self.datax = e.x
            self.datay = e.y
        #print(f"startx: {self.startx}, starty: {self.starty}")
        #print(f"datax: {self.datax}, starty: {self.datay}")
            
            
    #allow drag
    def plot_mouse_move(self, e):
        #note the xdata gets the position in the graph --good for matplotlib
        #note the x gets the position in pixels from left and bottom of axes --good for pyqt
        if e.inaxes and self.tracking:
            pos = (e.xdata, e.ydata)
            self.lastx = e.xdata
            self.lasty = e.ydata
            self.dataLastx = e.x
            self.dataLasty = e.y
            self.create_area(pos)
    
    #release stop tracking
    def plot_mouse_release(self, e):
        self.tracking = False
        
    #build EM plot
    def build_EM(self):
        #self.ax.clear() # discards the old graph
        #get data
        energies = get_energies(self.path, self.dat)
        #set range and plot
        self.energiesLow = energies[0]
        self.energiesHigh = energies[len(energies)-1]
        self.ax.imshow(self.result, cmap='gray', extent=[0, self.result.shape[1], 
                                                         self.energiesLow, self.energiesHigh])
        #remap to the energies of the experiment
        self.ax.set_aspect(self.result.shape[1] / (energies[len(energies)-1] - energies[0]))
        # refresh canvas
        self.configure_graph()
        self.canvas.draw()
    
    #create the boxed area
    def create_area(self, pos):
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
    def configure_graph(self):
        configure_graph_com(self, 'Energy vs Momentum', 'Momentum', 'Energy')
        
    #integrate over x or y
    def integrate(self):
        if self.sender() == self.intXButton:
            type = "EDC"
        else:
            type = "MDC"
        #create new window
        if(self.datax is None or self.datay is None or self.dataLastx is None or self.dataLasty is None):
            print("no box")
            self.datax = 0
            self.datay = self.result.shape[0]
            self.dataLastx = self.energiesLow
            self.dataLasty = self.energiesHigh
        #print(f"startx: {self.datax}, starty: {self.datay}, lastx: {self.dataLastx}, lasty: {self.dataLasty}")
        print(f"startx: {self.startx}, starty: {self.starty}, lastx: {self.lastx}, lasty: {self.lasty}")
        self.w = DistCrve(self.result, type, 
                          (self.startx, self.starty), (self.lastx, self.lasty), 
                          #(self.datax, self.datay), (self.dataLastx, self.dataLasty), 
                          self.energiesLow, self.energiesHigh)
        self.w.show()
         
    #save the file
    def save_file(self):
        save_file_com(self, self.result)
    
    #throws error dialogue 
    def error_dialogue(self, title, message):
        error_dialogue_com(self, title, message)
        return False
         
        