from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider, QRadioButton, QFileDialog, QCheckBox, QButtonGroup, QGraphicsView, QLineEdit
from PyQt6.QtGui import QMouseEvent, QPixmap, QPainter, QPen, QColor, QIntValidator
from PyQt6.QtCore import Qt, QDir
from tifConv import tiffIm
from PIL import Image, ImageQt
import numpy as np
import os, sys

class RIXSGUI(QMainWindow):
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
        
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 9)
        self.textLineX.setValidator(onlyInt)  
        self.textLineY.setValidator(onlyInt)
        self.textLineFinalX.setValidator(onlyInt)
        self.textLineFinalY.setValidator(onlyInt)
        
        self.textLineX.setMaxLength(4)
        self.textLineY.setMaxLength(4)
        self.textLineFinalX.setMaxLength(4)
        self.textLineFinalY.setMaxLength(4)
        self.textLineX.setPlaceholderText("Enter Starting X")
        self.textLineY.setPlaceholderText("Enter Starting Y")
        self.textLineFinalX.setPlaceholderText("Enter Ending X")
        self.textLineFinalY.setPlaceholderText("Enter Ending Y")
        parenLabel = QLabel("(")
        paren2Label = QLabel(")")
        commaLabel = QLabel(",")
        parenLabel2 = QLabel("(")
        paren2Label2 = QLabel(")")
        commaLabel2 = QLabel(",")
        
        #widget.setReadOnly(True) # uncomment this to make readonly
        
        self.radio_button1.clicked.connect(self.makeLine)
        self.radio_button1.clicked.connect(self.toggleRadioButton)
        self.textLineX.textChanged.connect(self.text_changed)
        
        
        layoutCol2.addWidget(self.radio_button1)

        layoutCol2Row1.addWidget(parenLabel)
        layoutCol2Row1.addWidget(self.textLineX)
        layoutCol2Row1.addWidget(commaLabel)
        layoutCol2Row1.addWidget(self.textLineY)
        layoutCol2Row1.addWidget(paren2Label)
        
        layoutCol2Row2.addWidget(parenLabel2)
        layoutCol2Row2.addWidget(self.textLineFinalX)
        layoutCol2Row2.addWidget(commaLabel2)
        layoutCol2Row2.addWidget(self.textLineFinalY)
        layoutCol2Row2.addWidget(paren2Label2)
        
        
        #layoutCol2.addWidget(self.radio_button2)
        #layoutCol2.addWidget(self.radio_button3)
        
        
        
        
        
        
        
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
        
    def slopedLine(self, p1, p2): #given points p1 and p2 which should be the slope of the line (unit vector?)
        result = np.zeros(self.tifArr[0].shape)
        for x in range(len(self.tifArr[0])):
            for y in range(len(self.tifArr[0])):
                result
    
    def toggleRadioButton(self):
        if self.radio_button1.isChecked():
            self.buttonGroup.setExclusive(False)
            self.radio_button1.setChecked(False)
            self.buttonGroup.setExclusive(True)
        else:
            self.radio_button1.setChecked(True)
                
    def makeLine(self):
        return
    




    def set_pen_color(self, c):
        self.pen_color = QColor(c)
      
    
    def mousePressEvent(self, e):
        #print("mouse press")
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
        

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
        
    def makeLine(self, pos):
        painter = QPainter()
        pixmap = self.image_label.pixmap()
        #p.setColor(self.pen_color)
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
        
    def text_changed(self, s):
        