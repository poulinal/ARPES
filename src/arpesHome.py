### 2024 Alex Poulin
from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider, QSplitter
from PyQt6.QtWidgets import QFileDialog, QGraphicsView, QMessageBox
from PyQt6.QtWidgets import QLineEdit, QPushButton, QComboBox, QCheckBox, QDialog
from PyQt6.QtCore import Qt, QDir, QPoint, pyqtSignal, QSettings
# from src.tifConv import tiff_im, get_info, get_energies
from src.energyVmomentum import EnergyVMomentum
import numpy as np

from src.widgets.colorramp import ColorRampWidget
from src.commonWidgets import reset_button_com, setup_figure_com, configure_graph_com, save_button_com
import matplotlib.pyplot as plt
from src.saveMov import ArrayToVideo
from src.widgets.arpesGraph import arpesGraph
from src.arpesData import arpesData
from src.fileWork import filesWidget

from src.widgets.lineCoordsWidget import lineCoordsWidget
from src.widgets.sliderWidget import EnergySliderWidget
from src.widgets.saveWidget import saveWidget
from src.widgets.manualEnergyInput import ManualEnergyInputWidget
from src.widgets.filterOptionsWidget import FilterOptionsWidget

np.set_printoptions(precision=4, suppress=True, threshold=5, linewidth=120)


###Todo note that current i have duplicate tif/energy arrays in both filework and arpesdata... try to consolidate one way or the other... probabl consoldate data from filework into only arpesdata

class ARPESHome(QWidget):
    openEVM = pyqtSignal(object, object, object)  # Signal to open EVM with the result data
    #resultEVMData, energiesArr, tifArr
    
    def __init__(self):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        
        # self.setGeometry(100, 100, 1024, 824)  # Window size
        #window size where the first two are the position of the window and the last two are the size of the window (width, height)
        self.settings = QSettings('DeLTA', 'ARDA')
        # Load last directory
        self.last_directory = self.settings.value('lastDirectory', '')
        
        #setup variables
        # self._plot_ref = [None, None] #first is main plot, second is line

        # Set up the main window
        # self.setWindowTitle("ARDA - Alexander Poulin")
        # self.central_widget = QWidget()
        # self.setCentralWidget(self.central_widget)

        layoutRow1, self.layoutCol1Row1, self.layoutCol1Row2, self.layoutCol1Row3 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        self.layoutCol2Row1, self.layoutCol2Row2, self.layoutCol2Row3, self.layoutCol2Row4 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        self.layoutCol2Row5, self.layoutCol2Row6 = QHBoxLayout(), QHBoxLayout()
        self.layoutCol1, self.layoutCol1Row2Col1, self.layoutCol2, self.layoutCol2Col1 = QVBoxLayout(), QVBoxLayout(), QVBoxLayout(), QVBoxLayout()
        
        #setup the UI
        self.setup_UI()
        
        #finalize layout
        layoutMainSplitter = QSplitter(Qt.Orientation.Horizontal)
        layoutMainSplitter.setHandleWidth(1)  # Make it wider (default is ~3px)
        layoutMainSplitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #6a6a6a;
                border: 1px solid #585757;
            }
            QSplitter::handle:hover {
                background-color: #5dade2;
            }
            QSplitter::handle:pressed {
                background-color: #2B2B2B;
            }
        """)

        self.layoutCol1.addLayout(self.layoutCol1Row1)
        self.layoutCol1.addLayout(self.layoutCol1Row2)
        self.layoutCol1Row2.addLayout(self.layoutCol1Row2Col1)
        self.layoutCol1.addLayout(self.layoutCol1Row3)
        col1Widget = QWidget()
        col1Widget.setLayout(self.layoutCol1)
        layoutMainSplitter.addWidget(col1Widget)
        
        self.layoutCol2Col1.addLayout(self.layoutCol2Row1)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row2)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row3)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row4)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row5)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row6)
        self.layoutCol2.addLayout(self.layoutCol2Col1)
        col2Widget = QWidget()
        col2Widget.setLayout(self.layoutCol2)
        layoutMainSplitter.addWidget(col2Widget)
        
        layoutRow1.addWidget(layoutMainSplitter)
        # self.central_widget.setLayout(layoutRow1)
        self.setLayout(layoutRow1)

    #setup the basic ui elements
    def setup_UI(self):
        self.arpesDataObj = arpesData() #this is a class that holds the data for the arpes
        
        #filter options toggle checkbox
        self.filterOptionsToggle = QPushButton("▶ Show Filter Options")
        self.filterOptionsToggle.setCheckable(True)
        self.filterOptionsToggle.setChecked(False)
        self.filterOptionsToggle.clicked.connect(self.toggleFilterOptions)
        self.filterOptionsWidget = FilterOptionsWidget()
        self.filterOptionsWidget.hide() #start hidden
        self.filterOptionsWidget.gaussianFilter.connect(lambda state, sigma: self.setGaussianFilter(state, sigma))
        self.layoutCol2Row2.addWidget(self.filterOptionsToggle)
        self.layoutCol2Row2.addWidget(self.filterOptionsWidget)
        
        #Main figure
        self.arpesGraphFig = arpesGraph() #this is a widget class that holds the graph
        self.arpesGraphFig.update_im(self.arpesDataObj.getCurrentTif(self.filterOptionsWidget.getGaussianToggle(), self.filterOptionsWidget.getGaussianSigma()))
        self.arpesGraphFig.setup_lincut_buttons()
        self.arpesGraphFig.setup_draggableText()
        
        self.layoutCol1Row2Col1.addWidget(self.arpesGraphFig)
        
        #setup energy slider
        self.energySlider = EnergySliderWidget()
        self.layoutCol1Row2Col1.addWidget(self.energySlider)
        self.energySlider.getSlider().valueChanged.connect(self.slider_value_changed) #on change, call slider_value_changed
        
        
        #setup file manager widget
        self.filesWidget = filesWidget()
        self.filesWidget.setFolderPathText(self.last_directory) #set the last directory
        self.layoutCol1Row1.addWidget(self.filesWidget)
        
        #setup submit button
        submitButton = QPushButton("Submit")
        submitButton.setFixedSize(200, 100)  # Set the fixed size of the button to create a square shape
        submitButton.clicked.connect(lambda : self.create_evm())
        self.layoutCol2Row5.addWidget(submitButton)
        
        #setup infoHead
        self.info = QLabel(self.filesWidget.getDatInfoFull())
        self.info.setStyleSheet("border: 1px solid white;")
        #current energy level
        self.currentEnergy = QCheckBox(f"Current Energy Level: {self.arpesDataObj.getCurrentEnergy()[0]}")
        self.currentEnergy.stateChanged.connect(lambda checked: self.arpesGraphFig.toggleEnergyText(checked))
        self.setupCurEnergy(0)
        self.layoutCol2Row1.addWidget(self.info)
        self.layoutCol2Row2.addWidget(self.currentEnergy)
        
        
        #setup line coords widget
        self.lineCoords = lineCoordsWidget()
        self.arpesGraphFig.mouse_graphpos_change.connect(lambda lastx, lasty: self.draw_line(lastx, lasty))
        self.arpesGraphFig.mouse_graphpos_start.connect(lambda startx, starty: self.lineCoords.setTexts(startX = startx, startY = starty))
        self.lineCoords.lineCoordsEdited.connect(lambda startx, starty, lastx, lasty: self.update_line_from_linecoords(startx, starty, lastx, lasty))

        
        
        
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
        self.maxContrastInput.setText(f"{self.arpesGraphFig.getMaxContrast():.2f}")
        
        # Connect the slider signals
        self.contrast_slider.valueChanged.connect(lambda blackvalue, whitevalue: self.updateContrastMinMax(vmin=blackvalue, vmax=whitevalue, maxContrastText=self.maxContrastInput.text())) #the * unpacks the tuple
        self.maxContrastInput.editingFinished.connect(lambda: self.updateContrastMinMax(maxContrastText=self.maxContrastInput.text()))


        # Add widgets to layout
        contrastH1Layout.addWidget(self.contrast_slider)
        contrastH1Layout.setStretch(0, 1)
        contrastH2Layout.addWidget(self.label_vmin)
        contrastH2Layout.addWidget(self.label_vmax)
        contrastH2Layout.addWidget(self.maxContrastInput)
        contrastVLayout.addLayout(contrastH1Layout)
        contrastVLayout.addLayout(contrastH2Layout)
        self.layoutCol2Row4.addLayout(contrastVLayout)
        
        
        
        #create colormap selector
        self.colormap = QComboBox()
        self.colormap.addItems(plt.colormaps())
        self.colormap.setCurrentText("grey")
        self.layoutCol2Row5.addWidget(self.colormap)
        self.colormap.currentTextChanged.connect(self.arpesGraphFig.change_colormap)
        
        
        # setup signals/connections
        self.filesWidget.update_dir.connect(self.send_dir_data)
        self.filesWidget.update_flatfield_dir.connect(self.send_flatfield_data)
    
    
    
    
    def setupCurEnergy(self, num):
        self.arpesDataObj.setCurrentEnergy(num)
        self.currentEnergy.setText(f"Current Energy Level: {self.arpesDataObj.getCurrentEnergy()[0]}")
        self.arpesGraphFig.setEnergyText(self.arpesDataObj.getCurrentEnergy()[0])

    #get everything from folder and setup data paths and image arrays 
    def send_dir_data(self):
        self.filesWidget.get_folder()
        self.filesWidget.process_folder_data()
        
        ###Todo setup warning for when tifnames are gathered but tifArr fails for whatever reason, i.e. no wifi to onedrive
        
        if self.filesWidget.getDatPath() != "": ###TOdo do we want to keep this
            # print("non empty dat path: send_dir_data")
            self.filesWidget.get_energies_arr(self.filesWidget.getDirPath(), self.filesWidget.getDatPath())
            self.filesWidget.setInfoFromDat(self.filesWidget.getDirPath(), self.filesWidget.getDatPath())
            # self.energyArr = self.filesWidget.getEnergies()
            # print(f"energyArr from filesWidget: {self.filesWidget.getEnergies()}")
            self.arpesDataObj.setEnergyArr(self.filesWidget.getEnergies())
            # print(f"tifArr from filesWidget before: {self.filesWidget.getTiffArr()}")
            self.arpesDataObj.setTifArr(self.filesWidget.getTiffArr())
            # print(f"tifArr from filesWidget after: {self.filesWidget.getTiffArr()}")
        
        elif self.filesWidget.getTiffArr() != []:
            # print("No .DAT file found in directory... Manual Input then")
            QMessageBox.information(self, "No .DAT file found", "No .DAT file found in directory... Please input energy values manually.")
            self.arpesDataObj.setTifArr(self.filesWidget.getTiffArr())
                        
            manualEnergyInput = ManualEnergyInputWidget()
            
            while True:
                energyInputDialogCode = manualEnergyInput.exec()
                if energyInputDialogCode == QDialog.DialogCode.Accepted:  # Check if the dialog was accepted
                    start, end, spacing = manualEnergyInput.result
                    self.filesWidget.setEnergies(np.arange(start, end + spacing, spacing))
                    
                elif energyInputDialogCode == QDialog.DialogCode.Rejected:
                    print("User cancelled manual energy input.")
                    return
                
                if len(self.arpesDataObj.getTifData()) != len(self.filesWidget.getEnergies()):
                    # print(f"len tifArr: {len(self.arpesDataObj.getTifData())}, len energies: {len(self.filesWidget.getEnergies())}")
                    # return RuntimeError("Number of energies does not match number of tiff files!")
                    QMessageBox.warning(self, "Invalid Input", f"Number of energies does not match number of tiff files! energyLength: {len(self.filesWidget.getEnergies())} tiffArrayLength: {len(self.arpesDataObj.getTifData())}. Please input again.")
                else:
                    break
            
            self.arpesDataObj.setEnergyArr(self.filesWidget.getEnergies())
        else:
            print("WARNING: empty dat path: send_dir_data \n \n \n")
        
        
        self.arpesGraphFig.update_im(self.arpesDataObj.getCurrentTif(self.filterOptionsWidget.getGaussianToggle(), self.filterOptionsWidget.getGaussianSigma()), set_default_clim=True)
        # update maxcontrast to be 100% of the max value in the current tif since set_default_clim will set to np.max; was thinking at first 150 but just 100 for now
        self.maxContrastInput.setText(str(self.arpesGraphFig.getMaxContrast()))
        self.energySlider.enable(len(self.filesWidget.getEnergies()) - 1)
        self.info.setText(self.filesWidget.getDatInfoHeader())   
        
        self.slider_value_changed(0) #reset slider to 0 and update everything accordingly
        
        self.last_directory = self.filesWidget.getDirPath()
        self.settings.setValue('lastDirectory', self.last_directory)
        
        
    def toggleFilterOptions(self):
        if self.filterOptionsToggle.isChecked():
            self.filterOptionsToggle.setText("▼ Hide Filter Options")
            # self.layoutCol2Row2.addWidget(self.lineCoords)
            self.filterOptionsWidget.setVisible(True)
        else:
            self.filterOptionsToggle.setText("▶ Show Filter Options")
            # self.layoutCol2Row2.removeWidget(self.lineCoords)
            self.filterOptionsWidget.hide()
     
    def slider_value_changed(self, i):
        self.arpesDataObj.setCurrentEnergy(i)
        self.currentEnergy.setText(f"Current Energy Level: {self.arpesDataObj.getCurrentEnergy()[0]}")
        self.arpesGraphFig.setEnergyText(self.arpesDataObj.getCurrentEnergy()[0])
        self.arpesGraphFig.update_im(self.arpesDataObj.getCurrentTif(self.filterOptionsWidget.getGaussianToggle(), self.filterOptionsWidget.getGaussianSigma()))
        
    def setGaussianFilter(self, bool, sigma=0.0):
        self.arpesGraphFig.update_im(self.arpesDataObj.getCurrentTif(bool, sigma))
        
    def updateContrastMinMax(self, vmin = None, vmax = None, maxContrastText = None):
        if maxContrastText is None:
            maxContrastText = self.maxContrastInput.text()
            
        if vmin is None or vmax is None: #not defined in parameters, get it from update_max_contrast
            # print("updateContrastMinMax: vmin and vmax is none")
            vmin, vmax = self.arpesGraphFig.getCurrentVminVmax()
            
        self.arpesGraphFig.update_contrast(blackvalue = vmin, whitevalue = vmax)
        self.arpesGraphFig.update_maxcontrast(maxContrastText)
        # print(f"updateContrastMinMax: vmax, vmin: {vmax, vmin}")
        self.arpesGraphFig.update_im(self.arpesDataObj.getCurrentTif())
        self.updateVminVmaxTexts(vmin = vmin, vmax = vmax)
            
    def updateVminVmaxTexts(self, vmin = None, vmax = None):
        #vmin and vmax currently are data as percent of the max contrast
        if type(vmax) is float:
            vmaxScaled = vmax * self.arpesGraphFig.getMaxContrast()
            self.label_vmax.setText(f"Left: {vmaxScaled:.2f}")
        if type(vmin) is float:
            vminScaled = vmin * self.arpesGraphFig.getMaxContrast()
            self.label_vmin.setText(f"Right: {vminScaled:.2f}")
            
    def update_line_from_linecoords(self, startx, starty, lastx, lasty):
        self.lineCoords.setTexts(startX=startx, startY=starty, lastX=lastx, lastY=lasty)
        self.arpesGraphFig.make_line_across(self.lineCoords.getPos())
        self.arpesGraphFig.draw_graph()
        
    def draw_line(self, lastx, lasty):
        if np.count_nonzero(self.arpesDataObj.getTifData()) == 0:
            print("WARNING... tif data not yet set or all data is zeroed... exiting")
            return None
        if self.arpesGraphFig.getToggledLineCutMode() == False and self.arpesGraphFig.getToggledSegLineCutMode() == False:
            return None
        
        self.lineCoords.setTexts(lastX = lastx, lastY = lasty)
        
        if self.arpesGraphFig.getToggledLineCutMode() == True:
            self.arpesGraphFig.make_line_across(*self.lineCoords.getPos())
        elif self.arpesGraphFig.getToggledSegLineCutMode() == True:
            self.arpesGraphFig.make_line_partial(*self.lineCoords.getPos())
        self.arpesGraphFig.draw_graph()
    
    def create_evm(self):
        resultEVMdata = self.arpesDataObj.interpl(*self.lineCoords.getPos(), vmin = self.arpesGraphFig.getCurrentVminVmax()[0], vmax = self.arpesGraphFig.getCurrentVminVmax()[1], posExtended = self.arpesGraphFig.getPosExtended(), distance = self.arpesGraphFig.getPosExtendedDistance())
        
        # print(f"nonzero resultEVMdata: {np.count_nonzero(resultEVMdata)}")
        
        # self.open_evm(resultEVMdata)
        self.openEVM.emit(resultEVMdata, self.arpesDataObj.getEnergyArr(), self.arpesDataObj.getTifData())
        
    def send_flatfield_data(self):
        self.arpesDataObj.get_flatfield_data(self.filesWidget.getFlatfieldInfo()[0])
        self.energySlider.enable(len(self.filesWidget.getTifNames()) - 1)
        self.info.setText(self.filesWidget.getDatInfoHeader())   
        