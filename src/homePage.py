from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QGridLayout
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize

from src.arpesHome import ARPESGUI
from src.xps import XPSGUI

import os

class HOMEGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #''' 
        print("File location using os.getcwd():",  
            os.getcwd()) 
        #'''

        # Set window title
        self.setWindowTitle("DeLTA Home Page")
        #self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QGridLayout()

        # Create left button with image
        arpesButton = QPushButton()
        arpesButton.setIcon(QIcon('src/images/arpesDemo.png'))  # Set left picture #assume in ARPES directory
        #print(arpesButton.sizeHint())
        arpesButton.clicked.connect(self.arpes_button_clicked)  # Connect click signal
        #arpesButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        #arpesButton.setFixedSize(500,500)
        layout.addWidget(arpesButton, 0, 0, 3, 1)
        arpesButton.setIconSize(QSize(arpesButton.size()))  # Set icon size to button size
        #print(self.central_widget.sizeHint().width, self.central_widget.sizeHint().height)


        # Create right button with image
        xpsButton = QPushButton()
        xpsButton.setIcon(QIcon('src/images/xpsDemo.png'))  # Set right picture
        xpsButton.clicked.connect(self.xps_button_clicked)  # Connect click signal
        layout.addWidget(xpsButton, 0, 1, 3, 1)
        xpsButton.setIconSize(xpsButton.size())  # Set icon size to button size

        
        self.central_widget.setLayout(layout)

    def arpes_button_clicked(self):
        print("Left button clicked")
        self.w = ARPESGUI()
        self.w.show()
        self.close()

    def xps_button_clicked(self):
        print("Right button clicked")
        self.w = XPSGUI()
        self.w.show()
        self.close()