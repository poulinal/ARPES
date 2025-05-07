### 2024 Alex Poulin
from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider
from PyQt6.QtWidgets import QFileDialog, QGraphicsView 
from PyQt6.QtWidgets import QLineEdit, QPushButton, QComboBox, QCheckBox
from PyQt6.QtCore import Qt, QDir, QPoint
from src.tifConv import tiff_im, get_info
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

from scipy.ndimage import gaussian_filter


class ARPESHome(QMainWindow):
    def __init__(self):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        
        self.setGeometry(100, 100, 1024, 824)  # Window size
        #window size where the first two are the position of the window and the last two are the size of the window (width, height)
        
        #setup variables
        self.dir_path = ""  # Class variable to store the directory path
        self.tifArr = []  # Class variable to store the tiff images as an array
        self.startx = None
        self.starty = None
        self.lastx = None
        self.lasty = None
        self.tracking = False
        self.lastIm = 0
        self.maxcontrast = 10000
        # self._plot_ref = [None, None] #first is main plot, second is line
        self.iris = False
        self.gaussian = False

        # Set up the main window
        self.setWindowTitle("ARDA - Alexander Poulin")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layoutRow1, self.layoutCol1Row1, self.layoutCol1Row2, self.layoutCol1Row3 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        self.layoutCol2Row1, self.layoutCol2Row2, self.layoutCol2Row3, self.layoutCol2Row4 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        self.layoutCol2Row5, self.layoutCol2Row6 = QHBoxLayout(), QHBoxLayout()
        self.layoutCol1, self.layoutCol1Row2Col1, self.layoutCol2, self.layoutCol2Col1 = QVBoxLayout(), QVBoxLayout(), QVBoxLayout(), QVBoxLayout()
        
        #setup the UI
        self.setup_UI()
        #finalize layout
        self.layoutCol1.addLayout(self.layoutCol1Row1)
        self.layoutCol1.addLayout(self.layoutCol1Row2)
        self.layoutCol1Row2.addLayout(self.layoutCol1Row2Col1)
        self.layoutCol1.addLayout(self.layoutCol1Row3)
        layoutRow1.addLayout(self.layoutCol1)
        
        self.layoutCol2Col1.addLayout(self.layoutCol2Row1)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row2)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row3)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row4)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row5)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row6)
        self.layoutCol2.addLayout(self.layoutCol2Col1)
        layoutRow1.addLayout(self.layoutCol2)
        self.central_widget.setLayout(layoutRow1)

    #setup the basic ui elements
    def setup_UI(self):
        arpesDataObj = arpesData() #this is a class that holds the data for the arpes
        
        
        #Main figure
        arpesGraphFig = arpesGraph() #this is a widget class that holds the graph
        arpesGraphFig.update_graph(arpesDataObj.tifArr)
        
        self.layoutCol1Row2Col1.addWidget(arpesGraphFig.canvas)
        
        #setup file manager widget
        self.filesWidget = filesWidget()
        self.layoutCol1Row1.addWidget(self.filesWidget)
        self.files.update_dir.connect(self.get_dir_data)
        self.files.update_flatfield_dir.connect(self.get_flatfield_data)
        
        
        #add slider to slide through images
        self.slider = QSlider(Qt.Orientation.Horizontal) #create new horizontal slider
        if len(self.tif) <= 1:
            self.slider.setRange(0, 100)
            self.slider.setDisabled(True)
        else:
            self.slider.setRange(0, len(self.tif) - 1)  # Set the range of the slider to the number of images
        self.slider.valueChanged.connect(self.slider_value_changed) #on change, call slider_value_changed
        self.layoutCol1Row3.addWidget(self.slider, stretch=1)  # Add the slider to the layout with stretch=1 to make it take full width
        
        #setup submit button
        submitButton = QPushButton("Submit")
        submitButton.setFixedSize(200, 100)  # Set the fixed size of the button to create a square shape
        submitButton.clicked.connect(self.interpl)
        self.layoutCol2Row5.addWidget(submitButton)
        
        #setup infoHead
        self.info = QLabel(self.get_info())
        self.info.setStyleSheet("border: 1px solid white;")
        #current energy level
        self.currentEnergy = QLabel(f"Current Energy Level: {self.energyArr[0]}")
        self.setupCurEnergy(0)
        self.layoutCol2Row1.addWidget(self.info)
        self.layoutCol2Row2.addWidget(self.currentEnergy)
        
        #gaussian toggle checkbox
        self.gaussianToggle = QCheckBox("Apply Gaussian Filter")
        self.gaussianToggle.stateChanged.connect(self.toggleGaussian)
        self.layoutCol2Row2.addWidget(self.gaussianToggle)
        
        
        lineCoords = lineCoordsWidget()
        
        
        
        contrastVLayout = QVBoxLayout()
        contrastH1Layout = QHBoxLayout()
        contrastH2Layout = QHBoxLayout()
        
        # Create sliders
        self.contrast_slider = ColorRampWidget()
        
        # Create labels to display slider values
        self.label_left = QLabel("Left: 0.00")
        self.label_right = QLabel(f"Right: {self.maxcontrast:.2f}")
        self.maxConstrastInput = QLineEdit()
        self.maxConstrastInput.setFixedWidth(100)
        self.maxConstrastInput.setText(f"{self.maxcontrast:.2f}")
        
        # Connect the slider signals
        self.contrast_slider.valueChanged.connect(self.update_contrast)
        self.maxConstrastInput.editingFinished.connect(self.update_maxcontrast)

        # Add widgets to layout
        contrastH1Layout.addWidget(self.contrast_slider)
        contrastH1Layout.setStretch(0, 1)
        contrastH2Layout.addWidget(self.label_left)
        contrastH2Layout.addWidget(self.label_right)
        contrastH2Layout.addWidget(self.maxConstrastInput)
        contrastVLayout.addLayout(contrastH1Layout)
        contrastVLayout.addLayout(contrastH2Layout)
        self.layoutCol2Row4.addLayout(contrastVLayout)
        
        # Connect the mouse events
        arpesGraphFig.canvas.mpl_connect('button_press_event', self.plot_mouse_click)
        arpesGraphFig.canvas.mpl_connect('motion_notify_event', self.plot_mouse_move)
        arpesGraphFig.canvas.mpl_connect('button_release_event', self.plot_mouse_release)
        
        #create colormap
        self.colormap = QComboBox()
        self.colormap.addItems(plt.colormaps())
        self.layoutCol2Row5.addWidget(self.colormap)
        self.colormap.currentTextChanged.connect(self.change_colormap)
        
        save_button_com(self, "Save File")
        self.layoutCol2Row6.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_file)
        
        #setup resetbutton
        reset_button_com(self)
        self.layoutCol2Row6.addWidget(self.resetButton)
        
    
    #resets the line
    def reset_line(self):
        self.textLineX.setText("")
        self.textLineY.setText("")
        self.textLineFinalX.setText("")
        self.textLineFinalY.setText("")
        
        
        self.lastx = None
        self.lasty = None
        self.startx = None
        self.starty = None
        
        
        #self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
        self.resetButton.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")
        self.resetButton.hide()
        
        #self.ax.cla()
        #self._plot_ref[1] = None
        self._plot_ref[1].set_xdata(0)
        self._plot_ref[1].set_ydata(0)
        ############ note this is just a bandaid fix, not really good practice ###############3
        self.canvas.draw()
        
    #get infohead
    def get_info(self):
        if self.dir_path == "":
            return "No data loaded"
        infoHead = get_info(self.dir_path, self.dat)
        #print(f"infoHead: \n {infoHead}, \n {type(infoHead)}")
        #FILE_ID, EXPERIMENT_NAME, MEASUREMENT_NAME, TIMESTAMP, INSTITUTION, SAMPLE
        #columnsToInclude = ['FILE_ID*', 'EXPERIMENT_NAME*', 'MEASUREMENT_NAME*', 'TIMESTAMP*', 'INSTITUTION*', 'SAMPLE*']
        #self.infoStr = infoHead.apply(lambda row: row.astype(str).values, axis=1) #this is an ndArray
        #print(f"infoStr: \n {self.infoStr[0]}, \n {type(self.infoStr)}")
        infoHead = infoHead.to_string(index=False, header=False)
        return infoHead
    
    def setupCurEnergy(self, num):
        self.currentEnergy.setText(f"Current Energy Level: {self.energyArr[num]}")
    
    def getImage(self):
        if self.gaussian:
            return gaussian_filter(self.tifArr[self.lastIm], sigma = 1.5)
        else:
            return self.tifArr[self.lastIm]

    #(will updates the images) according to the slider value
    def slider_value_changed(self, i):
        self.lastIm = i
        self.imageBuilder.build_image(self, self.getImage())
        self.setupCurEnergy(i)
        '''
        if (self.lastx is not None and self.lasty is not None):
            self.make_line((self.lastx, self.lasty))
            '''
        
    #on text change, update the line
    def text_edited(self, s):
        if (self.lastx is not None and self.lasty is not None and self.startx is not None and self.starty is not None):
            #self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
            self.lastx = float(self.textLineFinalX.text())
            self.lasty = float(self.textLineFinalY.text())
            self.startx = float(self.textLineX.text())
            self.starty = float(self.textLineY.text())
            self.make_line((self.lastx, self.lasty))
    
    def show_new_image(self, result):
        self.w = EnergyVMomentum(result, self.dir_path, self.tifArr, self.dat)
        #w.result = result
        self.w.show()
        
    #save the file
    def save_file(self):
        ArrayToVideo(self.tifArr, self.vmin, self.vmax, self)
        
        
        