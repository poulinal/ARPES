### 2024 Alex Poulin
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog

from src.commonWidgets import error_dialogue_com, save_button_com, configure_graph_com
import src.fileWork
from src.tifConv import tiff_im, get_energies
import numpy as np
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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
        layoutRow = QHBoxLayout()
        
        files = src.fileWork.files()
        self.dir_path = files.dir_path
        self.dat = files.dat
        #self.energies = files.energies
        tif = files.tif
        self.tifArr = tiff_im(self.dir_path, tif)
        self.energyArr = get_energies(self.dir_path, self.dat)
        
        #setupFigureCom(self)
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        widthPixels = 2080
        heightPixels = 810
        dpi = self.figure.get_dpi()
        widthInches = widthPixels / dpi
        heightInches = heightPixels / dpi
        self.figure.set_size_inches(widthInches, heightInches)  
        self.ax = self.figure.add_subplot(111)
        
        self.result = np.stack((self.integrate()[0], self.energyArr), axis=-1)
        print(self.result)
        #print(self.energyArr)
        self.ax.plot(self.result, '-')
        self.configure_graph()

        
        save_button_com(self, "Save File")
        layoutRow.addWidget(self.save_button)
        #self.saveButton.clicked.connect(self.saveFile)
        
        layout.addLayout(layoutRow)
        layout.addWidget(self.canvas)
        
    def integrate(self):
        result = np.zeros(shape = (1, len(self.tifArr)))
        
        #print(np.sum(self.tifArr[0]))
        for i in range(len(self.tifArr)):
            #self.energyArr[i] = sum(self.tifArr[i].flatten())
            result[0][i] = np.sum(self.tifArr[i])
        return result
    
    #configure the graph
    def configure_graph(self):
        self.ax.set_title("Intensity vs Energy")
        self.ax.set_xlabel("Energy")
        self.ax.set_ylabel("Intensity")
        
    
    #save the file
    def save_file(self):
        #print(np.flip(self.result))
        df = pd.DataFrame(np.flip(self.result), columns =['Energy', 'Intensity']) 
        
        file_name, _ = QFileDialog.getSaveFileName(self,"Save File","","Excel File(*.xlsx)")#,options = options)
        if file_name:
            print(file_name)
            df.to_excel(file_name, index = False)
            return True
        else:
            return self.error_dialogue("Error", "File not saved")
        
    #throws error dialogue 
    def error_dialogue(self, title, message):
        error_dialogue_com(self, title, message)
        return False