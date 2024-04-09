from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider, QRadioButton, QFileDialog, QCheckBox
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QDir
from tifConv import tiffIm
from PIL import Image, ImageQt
import numpy as np
import os, sys

class RIXSGUI(QMainWindow):
    dir_path = ""  # Class variable to store the directory path
    tifArr = []  # Class variable to store the tiff images as an array
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DeLTA Lab ARPES GUI")
        #self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layoutRow1 = QHBoxLayout()
        layoutCol1 = QVBoxLayout()
        layoutCol2 = QVBoxLayout()

        self.setup_ui(layoutCol1, layoutCol2)
        
        layoutRow1.addLayout(layoutCol1)
        layoutRow1.addLayout(layoutCol2)
        self.central_widget.setLayout(layoutRow1)
        
        self.last_x, self.last_y = None, None
        self.pen_color = QColor('#000000')

    #setup the basic ui elements
    def setup_ui(self, layoutCol1, layoutCol2):
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
        
        im = Image.fromarray(self.tifArr[0])
        self.pixmap = QPixmap.fromImage(ImageQt.ImageQt(im)) #set image based on numpy array
        
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
        self.radio_button1 = QRadioButton("Pick Two Points")
        self.radio_button2 = QRadioButton("Manual Choose Two Points")
        self.radio_button3 = QRadioButton("Pick Slope")
        self.radio_button1.clicked.connect(self.makeLine)

        layoutCol2.addWidget(self.radio_button1)
        layoutCol2.addWidget(self.radio_button2)
        layoutCol2.addWidget(self.radio_button3)
        
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
        im = Image.fromarray(self.tifArr[i])
        pixmap = QPixmap.fromImage(ImageQt.ImageQt(im)) #set image based on numpy array
        self.image_label.setPixmap(pixmap)
        
    def slopedLine(self, p1, p2): #given points p1 and p2 which should be the slope of the line (unit vector?)
        result = np.zeros(self.tifArr[0].shape)
        for x in range(len(self.tifArr[0])):
            for y in range(len(self.tifArr[0])):
                result
                
    def makeLine(self):
        '''
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)
        #pen = QPen(QColor.red, 3)
        pen = QPen()
        painter.setPen(pen)
        painter.drawLine(10, 10, self.rect().width() -10 , 10)
        '''
        self.update()
    
    
    def paintEvent(self, event):
        painter = QPainter(self)
        #painter.begin(self.image_label.pixmap())
        pen = QPen()
        #pen.setColor(QColor('red'))
        painter.setPen(pen)
        #painter.drawLine(10, 10, self.rect().width() -10 , 10)
        painter.drawLine(10, 10, 30 , 10)
        painter.end()
    




    def set_pen_color(self, c):
        self.pen_color = QColor(c)

    def mouseMoveEvent(self, e):
        pos = e.position()
        if self.last_x is None: # First event.
            self.last_x = pos.x()
            self.last_y = pos.y()
            return # Ignore the first time.
        

        painter = QPainter(self.image_label.pixmap())
        p = painter.pen()
        p.setWidth(4)
        #p.setColor(self.pen_color)
        p.setColor(QColor('red'))
        painter.setPen(p)
        painter.device()
        painter.drawLine(self.last_x, self.last_y, pos.x(), pos.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = pos.x()
        self.last_y = pos.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None