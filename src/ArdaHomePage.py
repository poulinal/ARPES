### 2024 Alex Poulin
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

from src.arpesHome import ARPESHome
from src.arpesMainWindow import ARPESMainWindow
from src.xps import XPSGUI

import os

""" Purpose of this file is to create the home page of the application. It is simply to distinguish between ARPES and XPS. 
    The user can click on the ARPES button to go to the ARPES page, or the XPS button to go to the XPS page. """


class HOMEGUI(QMainWindow):
    def __init__(self, main_dir):
        super().__init__()
        
        # Set window title
        self.setWindowTitle("DeLTA Home Page")

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QGridLayout()

        # Create left button with image
        arpesButton = QPushButton()
        arpesButton.setIcon(QIcon('src/utilities/images/arpesDemo.png'))  # Set left picture #assume in ARPES directory
        arpesButton.clicked.connect(self.arpes_button_clicked)  # Connect click signal
        layout.addWidget(arpesButton, 0, 0, 3, 1)
        arpesButton.setIconSize(QSize(arpesButton.size()))  # Set icon size to button size


        # Create right button with image
        xpsButton = QPushButton()
        xpsButton.setIcon(QIcon('src/utilities/images/xpsDemo.png'))  # Set right picture
        xpsButton.clicked.connect(self.xps_button_clicked)  # Connect click signal
        layout.addWidget(xpsButton, 0, 1, 3, 1)
        xpsButton.setIconSize(xpsButton.size())  # Set icon size to button size

        
        self.central_widget.setLayout(layout)

    def arpes_button_clicked(self):
        # print("Left button clicked")
        # self.w = ARPESHome()
        self.w = ARPESMainWindow()
        self.w.show()
        self.close()

    def xps_button_clicked(self):
        # print("Right button clicked")
        self.w = XPSGUI()
        self.w.show()
        self.close()