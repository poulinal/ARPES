from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt6.QtGui import QIcon, QPixmap

from image import ARPESGUI
from commonWidgets import setupFigureCom
import buildImage
import fileWork
from tifConv import tiffIm, getEnergies

"""_summary_
    integrates over each energy level to compile total electrons detected
    outputs said data to a txt file - later add ability to do circle, square integration
"""
class XPSGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("XPS Electron Detection")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.vmin = None
        self.vmax = None
        self._plot_ref = [None, None] #first is main plot, second is line
        
        files = fileWork.files()
        self.dir_path = files.dir_path
        self.dat = files.dat
        #self.energies = files.energies
        tif = files.tif
        self.tifArr = tiffIm(self.dir_path, tif)
        
        self.energyArr = getEnergies(self.dir_path, self.dat)
        
        setupFigureCom(self)
        self.imageBuilder = buildImage.ImageBuilder()
        self.imageBuilder.buildImage(self, 0)
        self.ax.axis('off')  # Turn off axes
        self.ax.autoscale(False)
        
        self.integrate()

        
        layout.addWidget(self.canvas)
        
    def integrate(self):
        for i in range(len(self.energyArr)):
            self.energyArr[i] = sum(self.tifArr[i].flatten())