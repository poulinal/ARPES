### 2024 Alex Poulin
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget, QComboBox
from PyQt6.QtWidgets import QGraphicsView, QPushButton, QLineEdit, QCheckBox
from PyQt6.QtCore import pyqtSignal
import numpy as np

from src.widgets.filterOptionsWidget import FilterOptionsWidget
from src.distributionCurve import DistCrve
from src.tifConv import get_energies
from src.commonWidgets import save_button_com, save_file_com, error_dialogue_com, configure_graph_com, setup_figure_com, reset_button_com

from src.widgets.colorramp import ColorRampWidget
from src.widgets.arpesGraph import arpesGraph
from src.widgets.lineCoordsWidget import lineCoordsWidget

from matplotlib import pyplot as plt

from scipy.ndimage import gaussian_filter

class EnergyVMomentum(QWidget):
    openMDC = pyqtSignal(object, object) #first object is resultdata, second object is extent
    openEDC = pyqtSignal(object, object) #first object is resultdata, second object is extent

    def __init__(self, results, energies, tifArr):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        
        # self.setFixedSize(400, 300)  # Width: 400px, Height: 300px
        
        
        #setup variables
        self.evmData = results
        print(f"nonzero evmdata: {np.count_nonzero(self.evmData)}")
        # self.startx = None
        # self.starty = None
        # self.lastx = None
        # self.lasty = None
        # self.datax = None
        # self.datay = None
        # self.dataLastx = None
        # self.dataLasty = None
        # self.tracking = False
        # self.path = path
        self.tifArr = tifArr
        # self.dat = dat
        #self.info = info
        self.energies = energies
        self.energiesLow = self.energies[0]
        self.energiesHigh = self.energies[len(self.energies)-1]
        self.gaussian = False #duplicate code, eventually want to consolidate
        self.extent = [0, self.evmData.shape[1], self.energiesLow, self.energiesHigh]
        print(f"extent: {self.extent}")
        
        ##TODO not necessarily linearly spaced, need to fix this later
        self.extentXarr = np.linspace(self.extent[0], self.extent[1], self.evmData.shape[1])
        self.extentYarr = np.linspace(self.extent[2], self.extent[3], self.evmData.shape[0])
        print(f"extentXarr: {self.extentXarr}")
        print(f"extentYarr: {self.extentYarr}")
        
        
        # self.maxcontrast = 10000
        # self.vmin = None
        # self.vmax = None
        #self._plot_ref = [None, None]
        
        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        # self._plot_ref = [None, None, None, None]
        # print(f"self._plot_ref: {self._plot_ref}")
        
        #setup window
        # self.setWindowTitle("Energy vs Momentum Plot - Alexander Poulin")
        self.mainWindow = QVBoxLayout()
        self.layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol1.addStretch()
        self.layoutCol2 = QVBoxLayout()
        self.layoutBottomMostRow = QHBoxLayout()
        #setup_UI
        self.setup_UI()
        #finialize layout
        # self.layoutCol2.addWidget(self.canvas)
        self.layoutRow1.addLayout(self.layoutCol2)
        self.layoutRow1.addLayout(self.layoutCol1)
        self.mainWindow.addLayout(self.layoutRow1)
        self.mainWindow.addLayout(self.layoutBottomMostRow)
        
        self.setLayout(self.mainWindow)
        
    def setup_UI(self):
        # save_button_com(self, "Save File")
        # self.layoutCol1.addWidget(self.save_button)
        #filter options toggle checkbox
        self.filterOptionsToggle = QPushButton("▶ Show Filter Options")
        self.filterOptionsToggle.setCheckable(True)
        self.filterOptionsToggle.setChecked(False)
        self.filterOptionsToggle.clicked.connect(self.toggleFilterOptions)
        self.filterOptionsWidget = FilterOptionsWidget()
        self.filterOptionsWidget.hide() #start hidden
        self.filterOptionsWidget.gaussianFilter.connect(lambda state, sigma: self.setGaussianFilter(state, sigma))
        self.layoutCol1.addWidget(self.filterOptionsToggle)
        self.layoutCol1.addWidget(self.filterOptionsWidget)
        
        
        self.EVMGraphFig = arpesGraph()
        print(f"self.evmData.shape: {self.getEVMData(self.gaussian).shape}")
        print(f"EVM initial plot")
        self.EVMGraphFig.setup_boxcut_button()
        self.EVMGraphFig.update_im(im = self.getEVMData(self.gaussian), set_default_clim=True, extent = self.extent)
        
        
        self.layoutCol2.addWidget(self.EVMGraphFig, stretch=1)
        
        self.lineCoords = lineCoordsWidget()
        self.layoutCol1.addWidget(self.lineCoords)
        
        self.intXButton = QPushButton("Int over X")
        self.intXButton.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
        self.layoutCol1.addWidget(self.intXButton)
        self.intYButton = QPushButton("Int over Y")
        self.intYButton.setFixedSize(100, 50)  # Set the fixed size of the button to create a square shape
        self.layoutCol1.addWidget(self.intYButton)
        
        self.intXButton.clicked.connect(self.create_MDC)
        self.intYButton.clicked.connect(self.create_EDC)
        
        
        #setup contrast slider
        contrastVLayout = QVBoxLayout()
        contrastH1Layout = QHBoxLayout()
        contrastH2Layout = QHBoxLayout()
        
        # Create sliders
        self.contrast_slider = ColorRampWidget()
        
        # Create labels to display slider values
        self.label_vmin = QLabel("Left: 0.00")
        self.label_vmax = QLabel(f"Right: 0.00")
        self.maxContrastInput = QLineEdit()
        self.maxContrastInput.setFixedWidth(100)
        self.maxContrastInput.setText(f"{self.EVMGraphFig.getMaxContrast():.2f}")
        
        # Connect the slider signals
        self.contrast_slider.valueChanged.connect(lambda blackvalue, whitevalue: self.updateContrastMinMax(vmin=blackvalue, vmax=whitevalue, maxContrastText=self.maxContrastInput.text()))
        self.maxContrastInput.editingFinished.connect(lambda: self.updateContrastMinMax(maxContrastText=self.maxContrastInput.text()))
        
        self.EVMGraphFig.mouse_graphpos_change.connect(lambda lastx, lasty: self.draw_box(lastx, lasty))
        self.EVMGraphFig.mouse_graphpos_start.connect(
            lambda startx, starty: (
            self.lineCoords.setTexts(startX=startx, startY=starty)
            if self.EVMGraphFig.getToggledBoxCutMode() else None
            )
        )
        # self.lineCoords.lineCoordsEdited.connect(lambda startx, starty, lastx, lasty: self.update_line_from_linecoords(startx, starty, lastx, lasty))
        
        #create colormap selector
        self.colormap = QComboBox()
        self.colormap.addItems(plt.colormaps())
        self.layoutCol1.addWidget(self.colormap)
        self.colormap.currentTextChanged.connect(self.EVMGraphFig.change_colormap)

        # Add widgets to layout
        contrastH1Layout.addWidget(self.contrast_slider)
        contrastH1Layout.setStretch(0, 1)
        contrastH2Layout.addWidget(self.label_vmin)
        contrastH2Layout.addWidget(self.label_vmax)
        contrastH2Layout.addWidget(self.maxContrastInput)
        contrastVLayout.addLayout(contrastH1Layout)
        contrastVLayout.addLayout(contrastH2Layout)
        self.layoutBottomMostRow.addLayout(contrastVLayout)
        
    def setGaussianFilter(self, bool, sigma=1.0):
        self.EVMGraphFig.update_im(self.getEVMData(bool, sigma), extent=self.extent)
   
    def toggleFilterOptions(self):
        if self.filterOptionsToggle.isChecked():
            self.filterOptionsToggle.setText("▼ Hide Filter Options")
            # self.layoutCol2Row2.addWidget(self.lineCoords)
            self.filterOptionsWidget.setVisible(True)
        else:
            self.filterOptionsToggle.setText("▶ Show Filter Options")
            # self.layoutCol2Row2.removeWidget(self.lineCoords)
            self.filterOptionsWidget.hide()
        
    
    def draw_box(self, lastx, lasty):
        """Draw a box on the graph at the given coordinates."""
        #print(f"draw box at {lastx}, {lasty}")
        if self.EVMGraphFig.getToggledBoxCutMode():
            self.lineCoords.setLastTexts(lastX = lastx, lastY = lasty)
            # startx, starty, lastx, lasty = self.lineCoords.getPos()
            self.EVMGraphFig.create_area(*self.lineCoords.getPos())

    def updateContrastMinMax(self, vmin = None, vmax = None, maxContrastText = None):
        if maxContrastText is None:
            maxContrastText = self.maxContrastInput.text()
            
        if vmin is None or vmax is None: #not defined in parameters, get it from update_max_contrast
            # print("updateContrastMinMax: vmin and vmax is none")
            vmin, vmax = self.EVMGraphFig.getCurrentVminVmax()
        self.EVMGraphFig.update_contrast(blackvalue = vmin, whitevalue = vmax)
        self.EVMGraphFig.update_maxcontrast(maxContrastText)
        # print(f"updateContrastMinMax: vmax, vmin: {vmax, vmin}")
        self.EVMGraphFig.update_im(self.getEVMData(self.gaussian), extent = self.extent)
        self.updateVminVmaxTexts(vmin = vmin, vmax = vmax)
         
    def updateVminVmaxTexts(self, vmin = None, vmax = None):
        #vmin and vmax currently are data as percent of the max contrast
        if type(vmax) is float:
            vmaxScaled = vmax * self.EVMGraphFig.getMaxContrast()
            self.label_vmax.setText(f"Left: {vmaxScaled:.2f}")
        if type(vmin) is float:
            vminScaled = vmin * self.EVMGraphFig.getMaxContrast()
            self.label_vmin.setText(f"Right: {vminScaled:.2f}")
    
    def getEVMData(self, gaussian = False, sigma=1.5):
        """
        Returns the evmData, optionally applying a Gaussian filter.
        """
        if gaussian:
            return gaussian_filter(self.evmData, sigma=sigma)
        else:
            return self.evmData
         
    def create_MDC(self):
        startx, starty, lastx, lasty = self.lineCoords.getPos()
        if startx is None or starty is None or lastx is None or lasty is None:
            print("WARNING... startx, starty, lastx, lasty are None, exiting...")
            return None
        if startx == '' or starty == '' or lastx == '' or lasty == '':
            print("WARNING... startx, starty, lastx, lasty are empty strings, exiting...")
            return None
        startx = float(startx)
        starty = float(starty)
        lastx = float(lastx)
        lasty = float(lasty)
        resultMDC, yindexstart, yindexlast = self.EVMGraphFig.integrateY(self.evmData, startx, starty, lastx, lasty, self.extent, self.energies, self.extentXarr, self.extentYarr)
        if resultMDC is None:
            print("WARNING... resultMDC is none, exiting...")
            return None
        
        resultMDC = np.flip(resultMDC)
        self.openMDC.emit(resultMDC, [[self.extentXarr[int(startx)], self.extentXarr[int(lastx)]], [self.extentYarr[int(yindexstart)], self.extentYarr[int(yindexlast)]]])
        
    def create_EDC(self):
        startx, starty, lastx, lasty = self.lineCoords.getPos()
        if startx is None or starty is None or lastx is None or lasty is None:
            print("WARNING... startx, starty, lastx, lasty are None, exiting...")
            return None
        if startx == '' or starty == '' or lastx == '' or lasty == '':
            print("WARNING... startx, starty, lastx, lasty are empty strings, exiting...")
            return None
        startx = float(startx)
        starty = float(starty)
        lastx = float(lastx)
        lasty = float(lasty)
        
        resultEDC, yindexstart, yindexlast = self.EVMGraphFig.integrateX(self.evmData, startx, starty, lastx, lasty, self.extent, self.energies, self.extentXarr, self.extentYarr)
        if resultEDC is None:
            print("WARNING... resultEDC is none, exiting...")
            return None
        self.openEDC.emit(resultEDC, [[self.extentXarr[int(startx)], self.extentXarr[int(lastx)]], [self.extentYarr[int(yindexstart)], self.extentYarr[int(yindexlast)]]])
        
        
    def scale_point(point, old_min, old_max, new_min, new_max):
        """
        Scales a value from an old range [old_min, old_max] to a new range [new_min, new_max].
        """
        if old_max == old_min:
            raise ValueError("old_max and old_min cannot be equal")
        scaled = (point - old_min) / (old_max - old_min) * (new_max - new_min) + new_min
        return scaled
        