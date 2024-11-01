### 2024 Alex Poulin
#recipricsl dpsce #jahn-teller effect
from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider
from PyQt6.QtWidgets import QFileDialog, QGraphicsView 
from PyQt6.QtWidgets import QLineEdit, QPushButton, QComboBox, QCheckBox
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QIntValidator
from PyQt6.QtCore import Qt, QDir, QPoint
from src.tifConv import tiff_im, get_info
from src.energyVmomentum import EnergyVMomentum
from PIL import Image, ImageQt
import numpy as np
import os, sys
from src.widgets.colorramp import ColorRampWidget
from src.commonWidgets import reset_button_com, setup_figure_com, configure_graph_com, save_button_com
import src.buildImage
import src.fileWork
import matplotlib.pyplot as plt
from src.tifConv import get_energies
from src.saveMov import ArrayToVideo

from scipy.ndimage import gaussian_filter


class ARPESGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        
        #setup variables
        self.dir_path = ""  # Class variable to store the directory path
        self.tifArr = []  # Class variable to store the tiff images as an array
        self.startx = None
        self.starty = None
        self.lastx = None
        self.lasty = None
        self.tracking = False
        self.lastIm = 0
        self.vmin = None
        self.vmax = None
        self.maxcontrast = 10000
        self._plot_ref = [None, None] #first is main plot, second is line
        self.iris = False
        self.gaussian = False

        # Set up the main window
        self.setWindowTitle("ARDA")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol1Row1 = QHBoxLayout()
        self.layoutCol1Row2 = QHBoxLayout()
        self.layoutCol1Row3 = QHBoxLayout()
        self.layoutCol2 = QVBoxLayout()
        self.layoutCol2Col1 = QVBoxLayout()
        self.layoutCol2Row1 = QHBoxLayout()
        self.layoutCol2Row2 = QHBoxLayout()
        self.layoutCol2Row3 = QHBoxLayout()
        self.layoutCol2Row4 = QHBoxLayout()
        self.layoutCol2Row5 = QHBoxLayout()
        self.layoutCol2Row6 = QHBoxLayout()
        #setup the UI
        self.setup_UI()
        #finalize layout
        self.layoutCol1.addLayout(self.layoutCol1Row1)
        self.layoutCol1.addLayout(self.layoutCol1Row2)
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
        self.setup_data()
        
        #print(self.tifArr)
        
        #Main figure
        setup_figure_com(self)
        self.imageBuilder = src.buildImage.ImageBuilder()
        self.imageBuilder.build_image(self, self.tifArr[0])
        self.ax.axis('off')  # Turn off axes
        self.ax.autoscale(False)
        
        self.layoutCol1Row2.addWidget(self.canvas)
        #print(plt.colormaps())
        
        #setup file button
        self.files = src.fileWork.files()
        self.layoutCol1Row1.addWidget(self.files)
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
        
        
        #setup lineCoords
        self.textLineX = QLineEdit()
        self.textLineY = QLineEdit()
        self.textLineFinalX = QLineEdit()
        self.textLineFinalY = QLineEdit()
        coordWidgetList = [self.textLineX, self.textLineY, self.textLineFinalX, self.textLineFinalY]
        self.textLineX.textEdited.connect(self.text_edited)
        self.textLineY.textEdited.connect(self.text_edited)
        #its properties
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 9)
        for w in coordWidgetList:
            #w.setFixedWidth(15)
            w.setValidator(onlyInt)
            w.setMaxLength(4)
            if w == self.textLineX or w == self.textLineY:
                w.setPlaceholderText("Enter Starting X")
            else:
                w.setPlaceholderText("Enter Ending X")
        parenLabel = QLabel("(")
        paren2Label = QLabel(")")
        commaLabel = QLabel(",")
        parenLabel2 = QLabel("(")
        paren2Label2 = QLabel(")")
        commaLabel2 = QLabel(",")
        #add it to layout
        controlWidgetList = [parenLabel, self.textLineX, commaLabel, self.textLineY, paren2Label]
        controlWidgetList2 = [parenLabel2, self.textLineFinalX, commaLabel2, self.textLineFinalY, paren2Label2]
        for w in controlWidgetList:
            self.layoutCol2Row3.addWidget(w)
        for w in controlWidgetList2:
            self.layoutCol2Row3.addWidget(w)
        
        
        
        
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
        self.canvas.mpl_connect('button_press_event', self.plot_mouse_click)
        self.canvas.mpl_connect('motion_notify_event', self.plot_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.plot_mouse_release)
        
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
        
    def setup_data(self):
        self.tifArr = np.zeros((50, 1024, 1024))
        self.dat = ""
        self.tif = ["dummy data"]
        self.energyArr = np.arange(0, 5, 0.1)
        
        
    def get_dir_data(self):
        self.files.get_folder()
        self.dir_path = self.files.dir_path
        self.dat = self.files.dat
        print(f"dir_path: {self.dir_path}")
        #self.energies = files.energies
        self.tif = self.files.tif
        self.tifArr = tiff_im(self.dir_path, self.tif)
        #self.tifArr = plt.tonemap(self.tifArr)
        
        if self.dat != "":
            self.energyArr = get_energies(self.dir_path, self.dat)
        
        self.imageBuilder.build_image(self, self.getImage())
        self.slider.setEnabled(True)
        self.slider.setRange(0, len(self.tif) - 1)
        self.info.setText(self.get_info())
    
        
    def get_flatfield_data(self):
        self.files.get_folder()
        flatfield = self.files.flatfield_path
        if flatfield is not None:
            #print("doing flat field correction now")
            #print(f"before: {self.tifArr[0][0]}")
            flatfield_tif = self.files.flatfield_tif
            #print(f"flatfield from class: {self.files.flatfield_tif}")
            #print(f"flatfield: {flatfield_tif}")
            #print(f"flatfield path: {self.files.flatfield_path}")
            self.flatfield_arr = tiff_im(self.files.flatfield_path, flatfield_tif)
            #print(f"iris: {self.iris_flat_arr[0][0]}")
            #print(f"before: {self.tifArr}")
            if len(self.tifArr) != len(self.flatfield_arr):
                ff_index = 0
                for i in range(len(self.tifArr)):
                    if ff_index >= len(self.flatfield_arr):
                        ff_index = 0
                    self.tifArr[i] = np.divide(self.tifArr[i], self.flatfield_arr[ff_index])
                    ff_index += 1
            else:
                self.tifArr = np.divide(self.tifArr, self.flatfield_arr)
            #print(f"after: {self.tifArr}")
            #self.flatfield_dat = files.flatfield_dat
            #print(f"after: {self.tifArr[0][0]}")
            self.imageBuilder.build_image(self, self.getImage())
    
    
    
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
        
    def change_colormap(self, text):
        self._plot_ref[0].set_cmap(text)
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
        
    def toggleGaussian(self):
        self.gaussian = not self.gaussian
        self.imageBuilder.build_image(self, self.getImage())
    
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
            
    def update_contrast(self, blackvalue, whitevalue):
        #print(f"black: {blackvalue}, white: {whitevalue}")
        self.vmin = blackvalue * self.maxcontrast
        self.vmax = whitevalue * self.maxcontrast
        self.label_left.setText(f"Left: {self.vmin:.2f}")
        self.label_right.setText(f"Right: {self.vmax:.2f}")
        #self.slider_right.setMinimum(value)
        #self._plot_ref[0].set_clim(vmin=self.vmin)
        self.imageBuilder.build_image(self, self.getImage())
        #self.update()
    
    def update_maxcontrast(self):
        self.maxcontrast = float(self.maxConstrastInput.text())
        self.label_right.setText(f"{self.maxcontrast:.2f}")
    
    #start point on click
    def plot_mouse_click(self, e):
        self.resetButton.show()
        self.resetButton.setStyleSheet("")
        self.tracking = not self.tracking
        if e.inaxes:
            self.startx = e.xdata
            self.starty = e.ydata
            self.textLineX.setText(str(self.startx))
            self.textLineY.setText(str(self.starty))
        #print(f"startx: {self.startx}, starty: {self.starty}")
         
    def plot_mouse_move(self, e):
        if e.inaxes and self.tracking:
            #print("inaxes")
            pos = (e.xdata, e.ydata)
            self.lastx = e.xdata
            self.lasty = e.ydata
            self.make_line(pos)
            #print(f"lastx: {self.lastx}, lasty: {self.lasty}")
            
    #release stop tracking
    def plot_mouse_release(self, e):
        self.tracking = False
        
    #on text change, update the line
    def text_edited(self, s):
        if (self.lastx is not None and self.lasty is not None and self.startx is not None and self.starty is not None):
            #self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
            self.lastx = float(self.textLineFinalX.text())
            self.lasty = float(self.textLineFinalY.text())
            self.startx = float(self.textLineX.text())
            self.starty = float(self.textLineY.text())
            self.make_line((self.lastx, self.lasty))
    
    #draws the line  
    def make_line(self, pos):
        if (self.startx is None or self.starty is None or self.lastx is None or self.lasty is None):
            return
        
        posExt, distance = self.extend_line(pos)
        #posExt starts from top left to whereever the line ends
        
        if self._plot_ref[1] is None:
            plot_refs = self.ax.plot(posExt[0], posExt[1], '-', color='yellow')
            self._plot_ref[1] = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref[1].set_xdata(posExt[0])
            self._plot_ref[1].set_ydata(posExt[1])
        #print(f"x_ext: {posExt[0]}, y_ext: {posExt[1]}")
        
        self.textLineFinalX.setText(str(pos[0]))
        self.textLineFinalY.setText(str(pos[1]))
        
        self.canvas.draw()
    
    def extend_line(self, pos):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim() #this is max height then the minimum

        distance = np.sqrt((pos[0] - self.startx)**2 + (pos[1] - self.starty)**2)
        
        if self.startx == pos[0]: #verticle line
            x_ext = np.full(int(ylim[0] - ylim[1]), self.startx)
            y_ext = np.linspace(ylim[1], ylim[0], int(ylim[0] - ylim[1]))
            return (x_ext, y_ext), distance 
        
        fx = np.polyfit([self.startx, pos[0]], [self.starty, pos[1]], deg=1)
        fy = np.polyfit([self.starty, pos[1]], [self.startx, pos[0]], deg=1)
        
        #here start means where xintercept is, and final means where the line would intersect with the upperbound of the box (i.e. the right side for x)
        xfinal = np.poly1d(fy)(xlim[1])
        yfinal = np.poly1d(fx)(ylim[0]) 
        xstart = np.poly1d(fy)(xlim[0])
        ystart = np.poly1d(fx)(ylim[1])
        
        xstart = np.clip(xstart, xlim[0], xlim[1]) #make sure it doesn't go out of bounds
        ystart = np.clip(ystart, ylim[1], ylim[0])
        xfinal = np.clip(xfinal, xlim[0], xlim[1])
        yfinal = np.clip(yfinal, ylim[1], ylim[0])
        
        if (min(xstart, xfinal) == xlim[0] and max(xstart, xfinal) == xlim[1]):
            #horizontal
            distance = np.sqrt((xlim[0] - xlim[1])**2 + (ystart - yfinal)**2)
            x_ext = np.linspace(xstart, xfinal, int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        elif (min(ystart, yfinal) == ylim[1] and max(ystart, yfinal) == ylim[0]):
            #verticle
            distance = np.sqrt((xstart - xfinal)**2 + (ylim[1] - ylim[0])**2)
            y_ext = np.linspace(ystart, yfinal, int(distance))
            x_ext = np.poly1d(fy)(y_ext)
    
        elif (min(xstart, xfinal) == xlim[0] and min(ystart, yfinal) == ylim[1]):
            #left to top
            distance = np.sqrt((xlim[0] - max(xstart, xfinal))**2 + (max(ystart, yfinal) - ylim[1])**2)
            x_ext = np.linspace(xlim[0], max(xstart, xfinal), int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        elif (max(xstart, xfinal) == xlim[1] and max(ystart, yfinal) == ylim[0]):
            #right to bottom
            distance = np.sqrt((xlim[1] - min(xstart, xfinal))**2 + (ylim[0] - min(ystart, yfinal))**2)
            x_ext = np.linspace(min(xstart, xfinal), xlim[1], int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        elif (min(xstart, xfinal) == xlim[0] and max(ystart, yfinal) == ylim[0]):
            #left to bottom
            distance = np.sqrt((xlim[0] - max(xstart, xfinal))**2 + (min(ystart, yfinal) - ylim[0])**2)
            x_ext = np.linspace(xlim[0], max(xstart, xfinal), int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        elif (max(xstart, xfinal) == xlim[1] and min(ystart, yfinal) == ylim[1]):
            #right to top
            #print("right to top")
            distance = np.sqrt((xlim[1] - min(xstart, xfinal))**2 + (ylim[1] - max(ystart, yfinal))**2)
            x_ext = np.linspace(max(xstart, xfinal), xlim[0], int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        else:
            #print("\n\nelse\n\n")
            #throw exception?
            #pure horizontal
            distance = xlim[1] - xlim[0]
            x_ext = np.linspace(xlim[0], xlim[1], int(distance))
            y_ext = np.linspace(ystart, ystart, int(distance))
        
        return (x_ext, y_ext), distance
        
    #interpolate the line to go across the image
    def interpl(self): 
        if (self.lastx is None or self.lasty is None or self.startx is None or self.starty is None):
            return
        posExt, distance = self.extend_line((self.lastx, self.lasty))
        #print(f"posExt: {posExt}")
        if (posExt[0] is None or posExt[1] is None):
            return #make sure there is a line to interpolate
        
        #maybe add some checks here to dumbproof
        
        #only return those points in the array which align with x_new and y_new
        #result = np.zeros(shape = (len(posExt[0]), len(posExt[1]))) #this will eventually be converted to image so should be height by width (height is number of images, width is distance of selection)
        #result = np.zeros(shape = (int(len(self.tifArr)), int(distance)))
        result = np.zeros(shape = (int(len(self.tifArr)), self.tifArr[0].shape[0])) #note shape is row, col
        imIndex = 0
        print(f"posExt: {posExt}")
        for tiffIm in self.tifArr:
            for i in range(result.shape[1]):
                #data point on the exact point (note posExt[0] is x coordinates along line, posExt[1] is y coordinates along line)
                nearestXPix = int(posExt[0][i])
                nearestYPix = int(posExt[1][i])
                
                #gamma = self.distanceWeightedAverage(nearestXPix, nearestYPix, posExt[0], posExt[1], 2)
                #dataPoint = gamma * tiffIm[nearestXPix][nearestYPix]
                dataPoint = tiffIm[nearestXPix][nearestYPix]
                
                #posExt[0][i] gets the xpoint on that iteration
                
                cluster_data = 1 #amount of points we cluster --for average later
                #if (posExt[0][i] < 0 or posExt[0][i] >= 1024 or posExt[1][i] < 0 or posExt[1][i] >= 1024):
                #dataPoint += tiff_im[int(posExt[0][i])][int(posExt[1][i])]
                
                
                if (nearestXPix > 0): #can go to left for cluster
                    dataPoint += tiffIm[nearestXPix - 1][nearestYPix]
                    cluster_data += 1
                    
                    #diagonal left up and down
                    if (nearestXPix > 0): #can go to up for cluster
                        dataPoint += tiffIm[nearestXPix - 1][nearestYPix - 1]
                        cluster_data += 1
                    if (nearestXPix < self.tifArr[0].shape[0] - 1): #can go to down for cluster
                        dataPoint += tiffIm[nearestXPix - 1][nearestYPix + 1]
                        cluster_data += 1
                    
                if (nearestXPix < self.tifArr[0].shape[1] - 1): #can go to right for cluster
                    dataPoint += tiffIm[nearestXPix + 1][nearestYPix]
                    cluster_data += 1
                    
                    #diagonal right up and down
                    if (nearestXPix > 0): #can go to up for cluster
                        dataPoint += tiffIm[nearestXPix + 1][nearestYPix - 1]
                        cluster_data += 1
                    if (nearestYPix < self.tifArr[0].shape[0] - 1): #can go to down for cluster
                        dataPoint += tiffIm[nearestXPix + 1][nearestYPix + 1]
                        cluster_data += 1
                    
                if (nearestYPix > 0): #can go to up for cluster
                    dataPoint += tiffIm[nearestXPix][nearestYPix - 1]
                    cluster_data += 1
                
                if (nearestYPix < self.tifArr[0].shape[0] - 1): #can go to down for cluster
                    dataPoint += tiffIm[nearestXPix][nearestYPix + 1]
                    cluster_data += 1
                    
                if cluster_data > 1:
                    dataPoint = dataPoint / cluster_data
                
                
                
                if self.vmin is not None and self.vmax is not None:
                    #print(f"datapoint: {dataPoint}")
                    #dataPoint = (dataPoint - self.vmin) / (self.vmax - self.vmin)
                    dataPoint = np.clip(dataPoint, self.vmin, self.vmax)
                    #print(f"new datapoint: {dataPoint}")
                result[imIndex][i] = dataPoint
            imIndex += 1
            
            
        result = result.astype(float)
        #print(result)
        
        result = np.flip(result, axis=0)
        
        self.show_new_image(result)
        return
    
    def show_new_image(self, result):
        self.w = EnergyVMomentum(result, self.dir_path, self.tifArr, self.dat)
        #w.result = result
        self.w.show()
        
    #save the file
    def save_file(self):
        ArrayToVideo(self.tifArr, self.vmin, self.vmax, self)
        
        
        