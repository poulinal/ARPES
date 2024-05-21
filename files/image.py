### 2024 Alex Poulin
#recipricsl dpsce #jahn-teller effect
from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider
from PyQt6.QtWidgets import QFileDialog, QGraphicsView 
from PyQt6.QtWidgets import QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QIntValidator
from PyQt6.QtCore import Qt, QDir, QPoint
from tifConv import tiffIm, getInfo
from energyVmomentum import EnergyVMomentum
from PIL import Image, ImageQt
import numpy as np
import os, sys
from commonWidgets import resetButtonCom, setupFigureCom, configureGraphCom
import buildImage
import fileWork
from tifConv import getEnergies

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
        self._plot_ref = [None, None] #first is main plot, second is line

        # Set up the main window
        self.setWindowTitle("DeLTA Lab ARPES GUI")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol2 = QVBoxLayout()
        self.layoutCol2Col1 = QVBoxLayout()
        self.layoutCol2Row1 = QHBoxLayout()
        self.layoutCol2Row2 = QHBoxLayout()
        self.layoutCol2Row3 = QHBoxLayout()
        self.layoutCol2Row4 = QHBoxLayout()
        self.layoutCol2Row5 = QHBoxLayout()
        self.layoutCol2Row6 = QHBoxLayout()
        #setup the UI
        self.setupUI()
        #finalize layout
        layoutRow1.addLayout(self.layoutCol1)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row1)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row2)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row3)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row4)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row5)
        self.layoutCol2.addLayout(self.layoutCol2Row6)
        self.layoutCol2.addLayout(self.layoutCol2Col1)
        layoutRow1.addLayout(self.layoutCol2)
        self.central_widget.setLayout(layoutRow1)

    #setup the basic ui elements
    def setupUI(self):
        files = fileWork.files()
        self.dir_path = files.dir_path
        self.dat = files.dat
        #self.energies = files.energies
        tif = files.tif
        self.tifArr = tiffIm(self.dir_path, tif)
        
        self.energyArr = getEnergies(self.dir_path, self.dat)
        
        #print(self.tifArr)
        
        setupFigureCom(self)
        self.imageBuilder = buildImage.ImageBuilder()
        self.imageBuilder.buildImage(self, 0)
        self.ax.axis('off')  # Turn off axes
        self.ax.autoscale(False)
        self.layoutCol1.addWidget(self.canvas)
        
        #add slider to slide through images
        slider = QSlider(Qt.Orientation.Horizontal) #create new horizontal slider
        slider.setRange(0, len(tif) - 1)  # Set the range of the slider to the number of images
        slider.valueChanged.connect(self.slider_value_changed) #on change, call slider_value_changed
        self.layoutCol1.addWidget(slider, stretch=1)  # Add the slider to the layout with stretch=1 to make it take full width
        
        #setup resetbutton
        resetButtonCom(self)
        self.layoutCol2Row6.addWidget(self.resetButton)
        
        #setup submit button
        submitButton = QPushButton("Submit")
        submitButton.setFixedSize(200, 100)  # Set the fixed size of the button to create a square shape
        submitButton.clicked.connect(self.interpl)
        self.layoutCol2Row5.addWidget(submitButton)
        
        #setup infoHead
        self.info = QLabel(self.getInfo())
        self.info.setStyleSheet("border: 1px solid white;")
        #current energy level
        self.currentEnergy = QLabel(f"Current Energy Level: {self.energyArr[0]}")
        self.setupCurEnergy(0)
        self.layoutCol2Row1.addWidget(self.info)
        self.layoutCol2Row2.addWidget(self.currentEnergy)
        
        
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
        
        # Create sliders
        self.slider_left = QSlider(Qt.Orientation.Horizontal)
        self.slider_right = QSlider(Qt.Orientation.Horizontal)

        # Set slider ranges
        self.slider_left.setMinimum(0)
        self.slider_left.setMaximum(6499)
        self.slider_right.setMinimum(150000)
        self.slider_right.setMaximum(350000)

        # Create labels to display slider values
        self.label_left = QLabel("Left: 0")
        self.label_right = QLabel("Right: 100")

        # Add widgets to layout
        self.layoutCol2Row4.addWidget(self.slider_left)
        self.layoutCol2Row4.addWidget(self.slider_right)
        self.layoutCol2Row4.addWidget(self.label_left)
        self.layoutCol2Row4.addWidget(self.label_right)

        # Connect signals
        self.slider_left.valueChanged.connect(self.update_label_left)
        self.slider_right.valueChanged.connect(self.update_label_right)
        
        # Connect the mouse events
        self.canvas.mpl_connect('button_press_event', self.plotMouseClick)
        self.canvas.mpl_connect('motion_notify_event', self.plotMouseMove)
        self.canvas.mpl_connect('button_release_event', self.plotMouseRelease)
    
    #resets the line
    def resetLine(self):
        self.textLineX.setText("")
        self.textLineY.setText("")
        self.textLineFinalX.setText("")
        self.textLineFinalY.setText("")
        self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
        self.resetButton.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")
        #self.resetButton.hide()
        self.update()
        
    #get infohead
    def getInfo(self):
        infoHead = getInfo(self.dir_path, self.dat)
        #print(f"infoHead: \n {infoHead}, \n {type(infoHead)}")
        #FILE_ID, EXPERIMENT_NAME, MEASUREMENT_NAME, TIMESTAMP, INSTITUTION, SAMPLE
        #columnsToInclude = ['FILE_ID*', 'EXPERIMENT_NAME*', 'MEASUREMENT_NAME*', 'TIMESTAMP*', 'INSTITUTION*', 'SAMPLE*']
        #self.infoStr = infoHead.apply(lambda row: row.astype(str).values, axis=1) #this is an ndArray
        #print(f"infoStr: \n {self.infoStr[0]}, \n {type(self.infoStr)}")
        infoHead = infoHead.to_string(index=False, header=False)
        return infoHead
    
    def setupCurEnergy(self, num):
        self.currentEnergy.setText(f"Current Energy Level: {self.energyArr[num]}")

    #(will updates the images) according to the slider value
    def slider_value_changed(self, i):
        self.lastIm = i
        self.imageBuilder.buildImage(self, self.lastIm)
        self.setupCurEnergy(i)
        '''
        if (self.lastx is not None and self.lasty is not None):
            self.makeLine((self.lastx, self.lasty))
            '''
            
    def update_label_left(self, value):
        self.vmin = value / 100
        self.label_left.setText(f"Left: {self.vmin}")
        #self.slider_right.setMinimum(value)
        #self._plot_ref[0].set_clim(vmin=self.vmin)
        self.imageBuilder.buildImage(self, self.lastIm)
        #self.update()
    
    def update_label_right(self, value):
        self.vmax = value / 100
        self.label_right.setText(f"Right: {self.vmax}")
        #self._plot_ref[0].set_clim(vmax=self.vmax)
        self.imageBuilder.buildImage(self, self.lastIm)
        #self.slider_left.setMaximum(value - 1)
        #self.update()
    
    #start point on click
    def plotMouseClick(self, e):
        #self.resetButton.show()
        #self.resetButton.setStyleSheet("")
        self.tracking = not self.tracking
        if e.inaxes:
            self.startx = e.xdata
            self.starty = e.ydata
        #print(f"startx: {self.startx}, starty: {self.starty}")
         
    def plotMouseMove(self, e):
        if e.inaxes and self.tracking:
            #print("inaxes")
            pos = (e.xdata, e.ydata)
            self.lastx = e.xdata
            self.lasty = e.ydata
            self.makeLine(pos)
            #print(f"lastx: {self.lastx}, lasty: {self.lasty}")
            
    #release stop tracking
    def plotMouseRelease(self, e):
        self.tracking = False
        
    #on text change, update the line
    def text_edited(self, s):
        if (self.lastx is not None and self.lasty is not None):
            #self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
            self.lastx = int(self.textLineFinalX.text())
            self.lasty = int(self.textLineFinalY.text())
            self.makeLine((self.lastx, self.lasty))
    
    #draws the line  
    def makeLine(self, pos):
        if (self.startx is None or self.starty is None or self.lastx is None or self.lasty is None):
            return
        posExt = self.extendLine(pos)
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
    
    def extendLine(self, pos):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        distance = np.sqrt((pos[0] - self.startx)**2 + (pos[1] - self.starty)**2)

        x_ext = np.linspace(xlim[0], xlim[1], int(distance))
        p = np.polyfit([self.startx, pos[0]], [self.starty, pos[1]], deg=1)
        y_ext = np.poly1d(p)(x_ext)
        '''
        if any(y_ext) > ylim[1]:
            y_ext = np.linspace(ylim[0], ylim[1], int(distance))
            p = np.polyfit([self.startx, pos[0]], [self.starty, pos[1]], deg=1)
            x_ext = np.poly1d(p)(y_ext)
            '''
        
        
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        return (x_ext, y_ext)
        
    #interpolate the line to go across the image
    def interpl(self): 
        posExt = self.extendLine((self.lastx, self.lasty))
        print(posExt)
        if (posExt[0] is None or posExt[1] is None):
            return #make sure there is a line to interpolate
        
        #maybe add some checks here to dumbproof
        
        #only return those points in the array which align with x_new and y_new
        result = np.zeros(shape = (len(posExt[0]), len(posExt[1]))) #this will eventually be converted to image so should be height by width
        imIndex = 0
        for tiffIm in self.tifArr:
            for x in range(result.shape[1]):
                result[imIndex][x] = int(tiffIm[int(posExt[0][x])][int(posExt[1][x])])
            imIndex += 1
        result = result.astype(float)
        
        self.showNewImage(result)
        return
    
    def showNewImage(self, result):
        self.w = EnergyVMomentum(result, self.dir_path, self.tifArr, self.dat)
        #w.result = result
        self.w.show()
        
        