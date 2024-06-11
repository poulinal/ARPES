from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog

from commonWidgets import errorDialogueCom, saveButtonCom
import fileWork
from tifConv import tiffIm, getEnergies
import numpy as np
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import csv


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
        
        files = fileWork.files()
        self.dir_path = files.dir_path
        self.dat = files.dat
        #self.energies = files.energies
        tif = files.tif
        self.tifArr = tiffIm(self.dir_path, tif)
        self.energyArr = getEnergies(self.dir_path, self.dat)
        
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
        
        saveButtonCom(self, "Save File")
        layoutRow.addWidget(self.saveButton)
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
    
    #save the file
    def saveFile(self):
        '''
        with open('studentsq.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.result)
            
        file_name, _ = QFileDialog.getSaveFileName(self,"Save File","","Text Files(*.txt)")#,options = options)
        if file_name:
            f = open(file_name, 'w')
            np.set_printoptions(threshold=np.inf)
            f.write(np.array_str(text))
            self.setWindowTitle(str(os.path.basename(file_name)) + " - ARPES Analysis")
            f.close()
            np.set_printoptions()#revert to defautl
            return True
        else:
            return self.errorDialogue("Error", "File not saved")
        #saveFileCom(self, self.result)
        '''
        #print(np.flip(self.result))
        df = pd.DataFrame(np.flip(self.result), columns =['Energy', 'Intensity']) 
        
        file_name, _ = QFileDialog.getSaveFileName(self,"Save File","","Excel File(*.xlsx)")#,options = options)
        if file_name:
            print(file_name)
            df.to_excel(file_name, index = False)
            '''
            f = open(file_name, 'w')
            np.set_printoptions(threshold=np.inf)
            f.write(np.array_str(text))
            self.setWindowTitle(str(os.path.basename(file_name)) + " - ARPES Analysis")
            f.close()
            np.set_printoptions()#revert to defautl
            '''
            return True
        else:
            return self.errorDialogue("Error", "File not saved")
        
    #throws error dialogue 
    def errorDialogue(self, title, message):
        errorDialogueCom(self, title, message)
        return False