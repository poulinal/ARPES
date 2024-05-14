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
from commonWidgets import resetButtonCom

class ARPESGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        
        #setup variables
        self.dir_path = ""  # Class variable to store the directory path
        self.tifArr = []  # Class variable to store the tiff images as an array
        self.im = Image.fromarray(np.zeros((1,1)))
        self.startx = 0
        self.starty = 0
        self.lastx = 0
        self.lasty = 0
        self.tracking = False

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
        #setup the UI
        self.setupUI()
        #finalize layout
        layoutRow1.addLayout(self.layoutCol1)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row1)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row2)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row3)
        self.layoutCol2Col1.addLayout(self.layoutCol2Row4)
        self.layoutCol2.addLayout(self.layoutCol2Col1)
        layoutRow1.addLayout(self.layoutCol2)
        self.central_widget.setLayout(layoutRow1)

    #setup the basic ui elements
    def setupUI(self):
        #get the directory path
        #'''
        self.dir_path = self.getFolder()
        if not os.path.exists(self.dir_path):
            print("not a valid directory")
            sys.exit()
            #'''
        #while testing:
        #self.dir_path = '/Users/alexpoulin/Downloads/git/ARPES/exData/Sum'

        #get data from directory
        tif = []
        for f in os.listdir(self.dir_path):
            if f.endswith('.TIF'):
                #print(f)
                tif.append(f)
            if f.endswith('.DAT'):
                self.dat = f
            if f.endswith('.txt'):
                self.energies = f
        tif = sorted(tif)
        #####should we check data to make sure images match with number in .DAT??
        #if len(tif) > 0: blah blah blah
        tif.pop(0) #remove the first 0'th tif file which is just the sum of all
        '''we should keep in mind that not all may have a sum file, so we should check for that'''
        self.tifArr = tiffIm(self.dir_path, tif)
        
        #print(self.tifArr)
        
        #generate image
        self.image_label = QLabel("Tif Image Placeholder")
        self.im = Image.fromarray(self.tifArr[0])
        self.pixmap = QPixmap.fromImage(ImageQt.ImageQt(self.im)) #set image based on numpy array
        self.image_label.setPixmap(self.pixmap)
        self.layoutCol1.addWidget(self.image_label)
        
        #add slider to slide through images
        slider = QSlider(Qt.Orientation.Horizontal) #create new horizontal slider
        slider.setRange(0, len(tif) - 1)  # Set the range of the slider to the number of images
        slider.valueChanged.connect(self.slider_value_changed) #on change, call slider_value_changed
        self.layoutCol1.addWidget(slider, stretch=1)  # Add the slider to the layout with stretch=1 to make it take full width
        
        #setup resetbutton
        resetButtonCom(self)
        self.layoutCol2Row4.addWidget(self.resetButton)
        
        #setup submit button
        submitButton = QPushButton("Submit")
        submitButton.setFixedSize(200, 100)  # Set the fixed size of the button to create a square shape
        submitButton.clicked.connect(self.interpl)
        self.layoutCol2Row3.addWidget(submitButton)
        
        #setup infoHead
        self.info = QLabel(self.getInfo())
        self.info.setStyleSheet("border: 1px solid white;")
        
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
        self.layoutCol2Row1.addWidget(self.info)
        controlWidgetList = [parenLabel, self.textLineX, commaLabel, self.textLineY, paren2Label]
        controlWidgetList2 = [parenLabel2, self.textLineFinalX, commaLabel2, self.textLineFinalY, paren2Label2]
        for w in controlWidgetList:
            self.layoutCol2Row2.addWidget(w)
        for w in controlWidgetList2:
            self.layoutCol2Row2.addWidget(w)
        
        
        
    #returns the path of the folder selected by the user
    def getFolder(self):
        #print("Get folder")
        dir_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            directory=QDir().homePath(),
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        return dir_path
    
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

    #(will updates the images) according to the slider value
    def slider_value_changed(self, i):
        self.im = Image.fromarray(self.tifArr[i])
        pixmap = QPixmap.fromImage(ImageQt.ImageQt(self.im)) #set image based on numpy array
        self.image_label.setPixmap(pixmap)
        #keep line if it exists
        if (self.textLineX.text() != "" or self.textLineY.text() != "" or self.textLineFinalX.text() != "" or self.textLineFinalY.text() != ""):
            self.makeLine((self.lastx, self.lasty))
    
    #on click, start tracking
    def mousePressEvent(self, e):
        #self.resetButton.show()
        self.resetButton.setStyleSheet("")
        if (e.pos().x() - self.image_label.x() < 0 or e.pos().x() - self.image_label.x() > self.image_label.width() 
            or e.pos().y() - self.image_label.y() < 0 or e.pos().y() - self.image_label.y() > self.image_label.height()):
            return #return if not in bounds
        self.tracking = True
        self.startx = e.pos().x() - self.image_label.x()
        self.starty = e.pos().y() - self.image_label.y()
        
        self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
        self.textLineX.setText(str(self.startx))
        self.textLineY.setText(str(self.starty))
    
    #on release, stop tracking
    def mouseReleaseEvent(self, e):
        self.tracking = False
         
    #allow drag
    def mouseMoveEvent(self, e):
        if not self.tracking: # no click.
            return
        #print(e.pos().x() - self.image_label.x()) //this is the true position with respect to the picture
        if (e.pos().x() - self.image_label.x() < 0 or e.pos().x() - self.image_label.x() > self.image_label.width() 
            or e.pos().y() - self.image_label.y() < 0 or e.pos().y() - self.image_label.y() > self.image_label.height()):
            return #return if not in bounds
        
        self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
        self.makeLine((e.pos().x(), e.pos().y()))
        self.lastx = e.pos().x()
        self.lasty = e.pos().y()
        
    #on text change, update the line
    def text_edited(self, s):
        if (self.textLineX.text() != "" and self.textLineY.text() != "" and self.textLineFinalX.text() != "" and self.textLineFinalY.text() != ""):
            pos = (int(self.textLineX.text()), int(self.textLineY.text()))
            self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
            self.makeLine(pos)
    
    #draws the line  
    def makeLine(self, pos):
        painter = QPainter()
        pixmap = self.image_label.pixmap()
        painter.begin(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen()
        pen.setColor(QColor('yellow'))
        pen.setWidth(3)  # Increase the width of the pen to 3
        painter.setPen(pen)
        painter.device()

        if ((pos[0] - self.image_label.x()) - self.startx) == 0: #is verticle (note self.startx is local to image so we must make pos.x local)
            painter.drawLine(int(pos[0]), 0, 
                             int(pos[0]), int(self.image_label.height()))
        else: #is not verticle
            interceptY, rightMostY, intersectX, slope = self.getLineProp(pos[0], pos[1])
            painter.drawLine(int(0), int(interceptY), int(self.image_label.width()), int(rightMostY)) #painter should be given local coord
        painter.end()
        
        self.textLineFinalX.setText(str(pos[0] - self.image_label.x()))
        self.textLineFinalY.setText(str(pos[1] - self.image_label.y()))
        
        self.image_label.setPixmap(pixmap)
        self.update()
            
    def getLineProp(self, posx, posy):
        posn1 = QPoint(posx, posy) #global value since this is gained from mouse - this is last point dragged to
        slope = ((posn1.y() - self.image_label.y()) - self.starty) / ((posn1.x() - self.image_label.x()) - self.startx)
        interceptY = self.starty - (slope * self.startx)
        rightMostY = slope * (self.image_label.width() - self.image_label.x()) + interceptY
        if slope == 0:
            return interceptY, rightMostY, self.image_label.x(), slope
        else:
            intersectX = -interceptY / slope #from the top left corner
            return interceptY, rightMostY, intersectX, slope
        
    #interpolate the line to go across the image
    def interpl(self): 
        interceptY, rightMostY, intersectX, slope = self.getLineProp(int(self.textLineFinalX.text()), int(self.textLineFinalY.text()))
        if (self.textLineX.text() == "" or self.textLineY.text() == "" or self.textLineFinalX.text() == "" or self.textLineFinalY.text() == ""):
            return #make sure there is a line to interpolate
        height = self.image_label.height() - 1
        width = self.image_label.width() - 1
        rightmostY = max(min(rightMostY, height), 0)
        leftmostY = max(min(interceptY, height), 0)
        if slope == 0:
            leftmostX = 0
            rightmostX = width
        else:
            leftmostX = max(min((leftmostY-interceptY) / slope, width), 0)
            rightmostX = max(min((rightmostY-interceptY) / slope, width), 0)       
        posn1 = QPoint(int(leftmostX), int(leftmostY))
        posn2 = QPoint(int(rightmostX), int(rightmostY))
        #where posn1 is the starting point and posn2 is the ending point
        length = np.sqrt((posn2.x() - posn1.x())**2 + (posn2.y() - posn1.y())**2)
        xlen = int(length)
        ylen = len(self.tifArr)
        x_new = np.linspace(posn1.x(), posn2.x(), xlen)
        y_new = np.linspace(posn1.y(), posn2.y(), xlen)
        
        #maybe add some checks here to dumbproof
        
        #only return those points in the array which align with x_new and y_new
        result = np.zeros(shape = (ylen, xlen)) #this will eventually be converted to image so should be height by width
        imIndex = 0
        for tiffIm in self.tifArr:
            for x in range(result.shape[1]):
                result[imIndex][x] = int(tiffIm[int(x_new[x])][int(y_new[x])])
            imIndex += 1
        result = result.astype(float)
        
        self.showNewImage(result)
        return
    
    def showNewImage(self, result):
        #print("result")
        #print(result)
        #print(type(self.info))
        self.w = EnergyVMomentum(result, self.dir_path, self.tifArr, self.dat)
        #w.result = result
        self.w.show()
        
        