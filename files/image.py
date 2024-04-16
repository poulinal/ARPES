### 2024 Alex Poulin

from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider
from PyQt6.QtWidgets import QRadioButton, QFileDialog, QCheckBox, QButtonGroup, QGraphicsView 
from PyQt6.QtWidgets import QLineEdit, QPushButton
from PyQt6.QtGui import QMouseEvent, QPixmap, QPainter, QPen, QColor, QIntValidator
from PyQt6.QtCore import Qt, QDir, QPoint
from tifConv import tiffIm
from parser import parseFolder
from energyVmomentum import EnergyVMomentum
from PIL import Image, ImageQt
import numpy as np
import os, sys

class ARPESGUI(QMainWindow):
    dir_path = ""  # Class variable to store the directory path
    tifArr = []  # Class variable to store the tiff images as an array
    im = Image.fromarray(np.zeros((1,1)))
    startx = 0
    starty = 0
    
    def __init__(self):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        
        self.setWindowTitle("DeLTA Lab ARPES GUI")
        #self.setGeometry(100, 100, 800, 600)
        self.tracking = False

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layoutRow1 = QHBoxLayout()
        layoutCol1 = QVBoxLayout()
        layoutCol2 = QVBoxLayout()
        layoutCol2Col1 = QVBoxLayout()
        layoutCol2Row1 = QHBoxLayout()
        layoutCol2Row2 = QHBoxLayout()
        layoutCol2Row3 = QHBoxLayout()
        self.setup_ui(layoutCol1, layoutCol2, layoutCol2Col1, layoutCol2Row1, layoutCol2Row2, layoutCol2Row3)
        
        layoutRow1.addLayout(layoutCol1)
        layoutCol2Col1.addLayout(layoutCol2Row1)
        layoutCol2Col1.addLayout(layoutCol2Row2)
        layoutCol2Col1.addLayout(layoutCol2Row3)
        layoutCol2.addLayout(layoutCol2Col1)
        layoutRow1.addLayout(layoutCol2)
        self.central_widget.setLayout(layoutRow1)

    #setup the basic ui elements
    def setup_ui(self, layoutCol1, layoutCol2, layoutCol2Col1, layoutCol2Row1, layoutCol2Row2, layoutCol2Row3):
        '''
        self.dir_path = self.getFolder()
        if not os.path.exists(self.dir_path):
            print("not a valid directory")
            sys.exit()
            '''
        #while testing:
        self.dir_path = '/Users/alexpoulin/Downloads/ARPES/ARPES/For_Alex/Sum'
    
            
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
        #print(len(tif))
        tif.pop(0) #remove the first 0'th tif file which is just the sum of all
        self.tifArr = tiffIm(self.dir_path, tif)
        #print(len(self.tifArr))
        
        #####should we check data to make sure images match with number in .DAT??
        #if len(tif) > 0: blah blah blah
        
        # Add image placeholder
        self.image_label = QLabel("Tif Image Placeholder")
        
        self.im = Image.fromarray(self.tifArr[0])
        self.pixmap = QPixmap.fromImage(ImageQt.ImageQt(self.im)) #set image based on numpy array
        self.image_label.setPixmap(self.pixmap)
        #self.resize(int(self.pixmap.width() / 2), int(self.pixmap.height() / 2))
        layoutCol1.addWidget(QLabel("Tif Image"))
        layoutCol1.addWidget(self.image_label)
        
        # Add slider to slide through images
        slider = QSlider(Qt.Orientation.Horizontal) #create new horizontal slider
        slider.setRange(0, len(tif) - 1)  # Set the range of the slider to the number of images
        slider.valueChanged.connect(self.slider_value_changed) #on change, call slider_value_changed
        layoutCol1.addWidget(slider, stretch=1)  # Add the slider to the layout with stretch=1 to make it take full width
        
        # Create a square button
        submitButton = QPushButton("Submit")
        submitButton.setFixedSize(200, 100)  # Set the fixed size of the button to create a square shape
        submitButton.clicked.connect(self.interpl)
        layoutCol2Row3.addWidget(submitButton)
        
        self.textLineX = QLineEdit()
        self.textLineY = QLineEdit()
        self.textLineFinalX = QLineEdit()
        self.textLineFinalY = QLineEdit()
        coordWidgetList = [self.textLineX, self.textLineY, self.textLineFinalX, self.textLineFinalY]
        
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
        
        #widget.setReadOnly(True) # uncomment this to make readonly
        
        self.textLineX.textEdited.connect(self.text_edited)
        self.textLineY.textEdited.connect(self.text_edited)
        
        controlWidgetList = [parenLabel, self.textLineX, commaLabel, self.textLineY, paren2Label]
        controlWidgetList2 = [parenLabel2, self.textLineFinalX, commaLabel2, self.textLineFinalY, paren2Label2]
        for w in controlWidgetList:
            layoutCol2Row1.addWidget(w)
        for w in controlWidgetList2:
            layoutCol2Row2.addWidget(w)
        
        
        
        
        
        
        
        
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


    #(will updates the images) according to the slider value
    def slider_value_changed(self, i):
        self.im = Image.fromarray(self.tifArr[i])
        pixmap = QPixmap.fromImage(ImageQt.ImageQt(self.im)) #set image based on numpy array
        self.image_label.setPixmap(pixmap)
    
    #on click, start tracking
    def mousePressEvent(self, e):
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
        
        #later to keep the image from being redrawn gonna have to draw on a new pixmap, overlay, and save the drawing
        self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
        self.makeLine(e.pos())
        
    #on text change, update the line
    def text_edited(self, s):
        if (self.textLineX.text() != "" and self.textLineY.text() != "" and self.textLineFinalX.text() != "" and self.textLineFinalY.text() != ""):
            pos = QPoint(int(self.textLineX.text()), int(self.textLineY.text()))
            self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
            self.makeLine(pos)
        
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
        
        '''
        #print(f"pos: {pos.y() - self.image_label.y()}, {self.starty}")
        if ((pos.x() - self.image_label.x()) - self.startx) == 0: #is verticle (note self.startx is local to image so we must make pos.x local)
            painter.drawLine(int(pos.x()), 0, 
                             int(pos.x()), int(self.image_label.height()))
        else: #is not verticle
            interceptY, rightMostY, intersectX, slope = self.getLineProp(pos.x(), pos.y())
            painter.drawLine(int(0), int(interceptY), int(self.image_label.width()), int(rightMostY)) #painter should be given local coord
        '''
        if ((pos.x() - self.image_label.x()) - self.startx) == 0: #is verticle (note self.startx is local to image so we must make pos.x local)
            painter.drawLine(int(pos.x()), 0, 
                             int(pos.x()), int(self.image_label.height()))
        else: #is not verticle
            interceptY, rightMostY, intersectX, slope = self.getLineProp(pos.x(), pos.y())
            leftmostX, leftmostY, rightmostX, rightmostY = self.getLinePoints(interceptY, rightMostY, intersectX, slope)
            painter.drawLine(int(leftmostX), int(leftmostY), int(rightmostX), int(rightmostY))
        painter.end()
        
        self.textLineFinalX.setText(str(pos.x() - self.image_label.x()))
        self.textLineFinalY.setText(str(pos.y() - self.image_label.y()))
        
        self.image_label.setPixmap(pixmap)
        self.update()
            
    def getLineProp(self, posx, posy):
        posn1 = QPoint(posx, posy) #global value since this is gained from mouse - this is last point dragged to
        #y=mx+b
        #x=(y-b)/m
        #b=y-mx
        #m=(y2-y1)/(x2-x1)
        #print(f"posn1X {posn1.x()}, posn1Y {posn1.y()}, startx {self.startx}, starty {self.starty}")
        slope = ((posn1.y() - self.image_label.y()) - self.starty) / ((posn1.x() - self.image_label.x()) - self.startx)
        interceptY = self.starty - (slope * self.startx)
        rightMostY = slope * (self.image_label.width() - self.image_label.x()) + interceptY
        if slope == 0:
            return interceptY, rightMostY, self.image_label.x(), slope
        else:
            intersectX = -interceptY / slope #from the top left corner
            #print(f"intersectY {intersectY}, finalY {finalY}, intersectX {intersectX}, slope {slope}")
            return interceptY, rightMostY, intersectX, slope
    
    def getLinePoints(self, interceptY, rightMostY, intersectX, slope):
        if (self.textLineX.text() == "" or self.textLineY.text() == "" or self.textLineFinalX.text() == "" or self.textLineFinalY.text() == ""):
            return #make sure there is a line to interpolate
        height = self.image_label.height() - 1
        width = self.image_label.width() - 1
        
        #print(f"textX {self.textLineX.text()}, textY {self.textLineY.text()}")
        #print(f"textFinalX {self.textLineFinalX.text()}, textFinalY {self.textLineFinalY.text()}")
        #interceptY, rightMostY, intersectX, slope = self.getLineProp(int(self.textLineFinalX.text()), int(self.textLineFinalY.text()))
        print(f"intersectY {interceptY}, rightMostY {rightMostY}, intersectX {intersectX}, slope {slope}")
        
        rightmostY = max(min(rightMostY, height), 0)
        leftmostY = max(min(interceptY, height), 0)
        if slope == 0:
            leftmostX = 0
            rightmostX = width
        else:
            leftmostX = max(min((leftmostY-interceptY) / slope, width), 0)
            rightmostX = max(min((rightmostY-interceptY) / slope, width), 0)
        return leftmostX, leftmostY, rightmostX, rightmostY
        
            
    def interpl(self):        
        interceptY, rightMostY, intersectX, slope = self.getLineProp(int(self.textLineFinalX.text()), int(self.textLineFinalY.text()))
        leftmostX, leftmostY, rightmostX, rightmostY = self.getLinePoints(interceptY, rightMostY, intersectX, slope)
            
        #y=mx+b
        #x=(y-b)/m
        #posn1 = QPoint(int(min(leftmostX, rightmostX)), int(min(leftmostY, rightmostY)))
        #posn2 = QPoint(int(max(leftmostX, rightmostX)), int(max(leftmostY, rightmostY)))
        posn1 = QPoint(int(leftmostX), int(leftmostY))
        posn2 = QPoint(int(rightmostX), int(rightmostY))
        #where posn1 is the starting point and posn2 is the ending point
        print(posn1, posn2)
        
        x_new = np.linspace(posn1.x(), posn2.x(), len(self.tifArr))
        y_new = np.linspace(posn1.y(), posn2.y(), len(self.tifArr))
        #print(x_new, y_new)
        
        #check same size (they should always be the same size):
        if len(x_new) != len(y_new):
            print("error")
            return
        
        #only return those points in the array which align with x_new and y_new
        result = np.zeros(shape = (len(self.tifArr), len(self.tifArr)))
        #print(f"resultshape: {result.shape}")
        index = 0
        for tiffIm in self.tifArr:
            for i in range(len(result[0])):
                result[index][i] = int(tiffIm[int(x_new[i])][int(y_new[i])])
                #result, get say first row, then populate that first row
                #with tiffIm's points at x_new[i] and y_new[i]
            index += 1
        #result = result.astype(np.uint8)
        result = result.astype(float)
        
        self.showNewImage(result)
        return
    
    def showNewImage(self, result):
        #print("result")
       #print(result)
        self.w = EnergyVMomentum(result, self.dir_path)
        #w.result = result
        self.w.show()
        
        