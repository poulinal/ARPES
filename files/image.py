### 2024 Alex Poulin

from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider
from PyQt6.QtWidgets import QRadioButton, QFileDialog, QCheckBox, QButtonGroup, QGraphicsView 
from PyQt6.QtWidgets import QLineEdit, QPushButton
from PyQt6.QtGui import QMouseEvent, QPixmap, QPainter, QPen, QColor, QIntValidator
from PyQt6.QtCore import Qt, QDir, QPoint
from tifConv import tiffIm
from PIL import Image, ImageQt
import numpy as np
import os, sys

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layoutRow1 = QHBoxLayout()
        layoutCol1 = QVBoxLayout()
        layoutCol2 = QVBoxLayout()
        layoutCol2Col1 = QVBoxLayout()
        layoutCol2Row1 = QHBoxLayout()
        layoutCol2Row2 = QHBoxLayout()

        self.setup_ui(layoutCol1, layoutCol2, layoutCol2Col1, layoutCol2Row1, layoutCol2Row2)
        
        layoutRow1.addLayout(layoutCol1)
        layoutCol2Col1.addLayout(layoutCol2Row1)
        layoutCol2Col1.addLayout(layoutCol2Row2)
        layoutCol2.addLayout(layoutCol2Col1)
        layoutRow1.addLayout(layoutCol2)
        self.central_widget.setLayout(layoutRow1)
        
        self.last_x, self.last_y = None, None
        self.pen_color = QColor('#000000')

    #setup the basic ui elements
    def setup_ui(self, layoutCol1, layoutCol2, layoutCol2Col1, layoutCol2Row1, layoutCol2Row2):
        self.dir_path = self.getFolder()
        if not os.path.exists(self.dir_path):
            print("not a valid directory")
            sys.exit()
            
        tif = []
        for f in os.listdir(self.dir_path):
            if f.endswith('.TIF'):
                tif.append(f)
            if f.endswith('.DAT'):
                dat = f
        #print("files" + str(os.listdir(self.dir_path))  ) 
        #print("tif" + str(sorted(tif)))
        tif = sorted(tif)
        self.tifArr = tiffIm(self.dir_path, tif)
        
        #####should we check data to make sure images match with number in .DAT??
        
        # Add image placeholder
        self.image_label = QLabel("Tif Image Placeholder")
        #if len(tif) > 0: blah blah blah
        
        #print(self.dir_path + "/" + tif[0])
        #pixmap = QPixmap(self.dir_path + "/" + tif[0])  # Set your image path here  #this is to get image via dir path
        #self.image_label.setScaledContents(True)
        
        #print(self.tifArr[0])
        self.im = Image.fromarray(self.tifArr[0])
        self.pixmap = QPixmap.fromImage(ImageQt.ImageQt(self.im)) #set image based on numpy array
        
        self.image_label.setPixmap(self.pixmap)
        self.resize(int(self.pixmap.width() / 2), int(self.pixmap.height() / 2))
        layoutCol1.addWidget(QLabel("Tif Image"))
        layoutCol1.addWidget(self.image_label)
        
        # Add slider to slide through images
        slider = QSlider(Qt.Orientation.Horizontal) #create new horizontal slider
        slider.setRange(0, len(tif) - 1)  # Set the range of the slider to the number of images
        slider.valueChanged.connect(self.slider_value_changed) #on change, call slider_value_changed
        layoutCol1.addWidget(slider, stretch=1)  # Add the slider to the layout with stretch=1 to make it take full width
        
        # Add radio buttons
        self.checkbox = QCheckBox("Energies Map")
        
        self.buttonGroup = QButtonGroup()
        self.radio_button1 = QRadioButton("Pick Two Points")
        self.buttonGroup.addButton(self.radio_button1)
        
        self.textLineX = QLineEdit()
        self.textLineY = QLineEdit()
        self.textLineFinalX = QLineEdit()
        self.textLineFinalY = QLineEdit()
        coordWidgetList = [self.textLineX, self.textLineY, self.textLineFinalX, self.textLineFinalY]
        
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 9)
        for w in coordWidgetList:
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
        
        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.interpl)
        
        
        layoutCol2.addWidget(self.radio_button1)
        
        controlWidgetList = [parenLabel, self.textLineX, commaLabel, self.textLineY]
        controlWidgetList2 = [paren2Label, parenLabel2, self.textLineFinalX, commaLabel2, self.textLineFinalY, paren2Label2]

        for w in controlWidgetList:
            layoutCol2Row1.addWidget(w)
        for w in controlWidgetList2:
            layoutCol2Row2.addWidget(w)
        
        layoutCol2.addWidget(self.submitButton)
        
        
        
        
        
        
        
        
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
        #print("Slider value changed")
        #print(self.tifArr[i])
        self.im = Image.fromarray(self.tifArr[i])
        pixmap = QPixmap.fromImage(ImageQt.ImageQt(self.im)) #set image based on numpy array
        self.image_label.setPixmap(pixmap)
    
    def mousePressEvent(self, e):
        #print("mouse press")
        if (e.pos().x() - self.image_label.x() < 0 or e.pos().x() - self.image_label.x() > self.image_label.width() or e.pos().y() - self.image_label.y() < 0 or e.pos().y() - self.image_label.y() > self.image_label.height()):
            return #return if not in bounds
        pos = e.pos()
        self.startx = pos.x() - self.image_label.x()
        self.starty = pos.y() - self.image_label.y()
        #if self.startx > int(self.image_label.x()) and self.startx < int(self.image_label.x()) + int(self.image_label.width() and self.starty > int(self.image_label.y()) and self.starty < int(self.image_label.y()) + int(self.image_label.height())):
        self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
        self.textLineX.setText(str(self.startx))
        self.textLineY.setText(str(self.starty))
         

    #allow drag
    def mouseMoveEvent(self, e):
        #print("mouse release")
        #print(e.pos().x() - self.image_label.x()) //this is the true position with respect to the picture
        if (e.pos().x() - self.image_label.x() < 0 or e.pos().x() - self.image_label.x() > self.image_label.width() or e.pos().y() - self.image_label.y() < 0 or e.pos().y() - self.image_label.y() > self.image_label.height()):
            return #return if not in bounds
        pos = e.pos()
        if self.last_x is None: # First event.
            #print("no last_x")
            self.last_x = pos.x()
            self.last_y = pos.y()
            return # Ignore the first time.
        #if self.startx < int(self.image_label.x()) and self.startx > int(self.image_label.x()) + int(self.image_label.width() and self.starty < int(self.image_label.y()) and self.starty > int(self.image_label.y()) + int(self.image_label.height())):
            #not in bounds
        #    return
        #else:
        #later to keep the image from being redrawn gonna have to draw on a new pixmap, overlay, and save the drawing
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
        
        #below is to draw a finite line
        #painter.drawLine(int(self.startx), int(self.starty), int(pos.x() - self.image_label.x()), int(pos.y() - self.image_label.y()))
        
        if ((pos.x() - self.image_label.x()) - self.startx) == 0:
            painter.drawLine(int(self.image_label.x()), int(self.image_label.y()), int(self.image_label.x() + self.image_label.width()), int(self.image_label.y() + self.image_label.height()))
        else:
            slope = ((pos.y() - self.image_label.y()) - self.starty) / ((pos.x() - self.image_label.x()) - self.startx)
            intersect = self.starty - slope * self.startx
            finaly = slope * self.image_label.width() + intersect
            #print("slope: " + str(slope))
            #print("intersect: " + str(intersect))
            painter.drawLine(int(self.image_label.x()), int(intersect), int(self.image_label.x() + self.image_label.width()), int(finaly))
        
        painter.end()
        
        self.textLineFinalX.setText(str(pos.x() - self.image_label.x()))
        self.textLineFinalY.setText(str(pos.y() - self.image_label.y()))
        
        self.image_label.setPixmap(pixmap)
        
        self.update()

        # Update the origin for next time.
        self.last_x = pos.x()
        self.last_y = pos.y()
        
    def text_edited(self, s):
        if (self.textLineX.text() != "" and self.textLineY.text() != "" and self.textLineFinalX.text() != "" and self.textLineFinalY.text() != ""):
            pos = QPoint(int(self.textLineX.text()), int(self.textLineY.text()))
            self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
            self.makeLine(pos)
            
            
            
    def getLine(self, startx, starty):
        posn1 = QPoint(startx, starty)
        
        slope = ((posn1.y() - self.image_label.y()) - self.starty) / ((posn1.x() - self.image_label.x()) - self.startx)
        intersect = self.starty - slope * self.startx
        finaly = slope * self.image_label.width() + intersect
        return QPoint(startx, starty), 
            
    def interpl(self):
        if (self.textLineX.text() == "" or self.textLineY.text() == "" or self.textLineFinalX.text() == "" or self.textLineFinalY.text() == ""):
            return
        posn1 = QPoint(int(self.textLineX.text()), int(self.textLineY.text()))
        posn2 = QPoint(int(self.textLineFinalX.text()), int(self.textLineFinalY.text()))
        #where posn1 is the starting point and posn2 is the ending point=
        x_new = np.linspace(posn1.x(), posn2.x(), len(self.tifArr))
        #go through the list of tiffim (tifarr)
        #y_new = np.interp(x_new, x, y) 
        y_new = np.linspace(posn1.y(), posn2.y(), len(self.tifArr))
        
        #print("x_new" + str(x_new))
        #print("y_new" + str(y_new))
        
        #check same size (they should always be the same size):
        if len(x_new) != len(y_new):
            print("error")
            return
        
        #only return those points in the array which align with x_new and y_new
        result = np.zeros(shape = (len(self.tifArr), len(self.tifArr)))
        index = 0
        for tiffIm in self.tifArr:
            #print("tiffIm: ")
            #print(tiffIm)
            #print(tiffIm[0][0])
            for i in range(len(result[0])):
                #print("i: ")
                '''
                print("f: ")
                print(type(tiffIm[int(x_new[i])][int(y_new[i])]))
                print("int: ")
                print(type(int(tiffIm[int(x_new[i])][int(y_new[i])])))
                '''
                result[index][i] = int(tiffIm[int(x_new[i])][int(y_new[i])])
                #result, get say first row, then populate that first row
                #with tiffIm's points at x_new[i] and y_new[i]
            index += 1
        result = result.astype(np.uint8)
        #print(result[0][0])
        #print(type(result[0][0]))
            
        #print(result)
        
        #plt.figure()
        #plt.imshow(result)
        #plt.show()
        self.showNewImage(result)
            
        return
    
    def showNewImage(self, result):
        #print("result")
       #print(result)
        self.w = EnergyVMomentum(result)
        #w.result = result
        self.w.show()
        
        

class EnergyVMomentum(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    #result = np.zeros((50,50))
    
    def __init__(self, results):
        super().__init__()
        QGraphicsView.__init__(self, parent=None)
        
        self.setWindowTitle("Energy vs Momentum Plot")
        
        #self.central_widget = QWidget()
        #self.setCentralWidget(self.central_widget)
        
        self.layoutRow1 = QHBoxLayout()
        self.layoutCol1 = QVBoxLayout()
        self.layoutCol2 = QVBoxLayout()
        
        self.label = QLabel("Another Window")
        #self.EM_label = QLabel("Placeholder Energy vs Momentum")
        self.layoutCol1.addWidget(self.label)
        #self.layoutCol2.addWidget(self.EM_label)
        self.result = results
        
        
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        
        self.show()
        self.buildEM()
        

        sliderX = QSlider(Qt.Orientation.Horizontal) #create new horizontal slider
        sliderY = QSlider(Qt.Orientation.Vertical) #create new horizontal slider
        sliderX.setRange(0, self.result.shape())  # Set the range of the slider to the width of the image
        sliderX.valueChanged.connect(self.slider_value_changed) #on change, call slider_value_changed
        
        layoutCol1.addWidget(slider, stretch=1)  # Add the slider to the layout with stretch=1 to make it take full width
        
        self.layoutCol2.addWidget(self.canvas)
        self.layoutRow1.addLayout(self.layoutCol1)
        self.layoutRow1.addLayout(self.layoutCol2)
        #self.central_widget.setLayout(self.layoutRow1)
        self.setLayout(self.layoutRow1)
        
    def buildEM(self):
        #print("self: ")
        #print(self.result)
        
        ''' this is for straight picture
        newIm = Image.fromarray(self.result)
        self.pixmap = QPixmap.fromImage(ImageQt.ImageQt(newIm))
        self.pixmap = self.pixmap.scaled(512, 512)
        print("pixmap: " + str(self.pixmap.width()) + " " + str(self.pixmap.height()))
        self.resize(int(self.pixmap.width() / 2), int(self.pixmap.height() / 2))
        self.EM_label.setPixmap(self.pixmap)
        '''
        
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        '''from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar'''
        #self.toolbar = NavigationToolbar(self.canvas, self)
        
        
        #this is for graph
        data = self.result

        
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()
        # plot data
        #ax.plot(data, '*-')
        
        ax.imshow(data, cmap='gray')
        ax.set_xlabel('Momentum')
        ax.set_ylabel('Energy') #recipricsl dpsce #jahn-teller effect
        ax.invert_yaxis()
        ax.set_title('Energy vs Momentum')
        ax.grid(True)

        # refresh canvas
        self.canvas.draw()
        

        
''' 
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.
'''