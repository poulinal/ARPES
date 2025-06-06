import os, sys

from PyQt6.QtWidgets import QFileDialog, QDialogButtonBox, QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QHBoxLayout, QGroupBox, QFileDialog, QWidget
from PyQt6.QtCore import QDir, pyqtSignal

from src.widgets.getfileordir import getOpenFilesAndDirs
from src.tifConv import tiff_im

import numpy as np
from PIL import Image
from pandas import read_csv as pd

class filesWidget(QWidget):
    
    update_dir = pyqtSignal(str)
    update_flatfield_dir = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        #get the directory path
        #'''
        self.setupWidget()
        self.tifNames= []
        self.tifArr = []
        self.dat = ""
        self.dir_path = ""
        self.infoFull = ""
        self.energies = []
        self.energiesValArr = []
        
        self.flatFieldDirPath = ""
        self.flatFieldNames = []
        self.flatFieldArr = []
        self.flatFieldDat = ""
        self.flatFieldEnergiesArr = [] #will use same index as self.energies... #Todo these should be same length but handle when not
        self.flatfield_correction = False
        
    #returns the path of the folder selected by the user
    def setupWidget(self):
        folder_menu_layout = QVBoxLayout()
        
        self.flatfield_correction = False
        flatfieldButton = QCheckBox('Check To Include Flat Field Correction')

        get_folder_layout = QHBoxLayout()
        self.folder_path = QLineEdit()
        push_browse = QPushButton('Browse')
        
        flatfield_get_folder_layout = QHBoxLayout()
        self.flatfield_folder_path = QLineEdit()
        self.flatfield_push_browse = QPushButton('Browse')
        
        flatfield_get_folder_layout.addWidget(self.flatfield_folder_path)
        flatfield_get_folder_layout.addWidget(self.flatfield_push_browse)
        flatfield_get_folder_layout.setEnabled(False)
        self.flatfield_folder_path.setVisible(False)
        self.flatfield_push_browse.setVisible(False)

        get_folder_layout.addWidget(self.folder_path)
        get_folder_layout.addWidget(push_browse)
        
        folder_menu_layout.addLayout(get_folder_layout)
        folder_menu_layout.addWidget(flatfieldButton)
        folder_menu_layout.addLayout(flatfield_get_folder_layout)
        
        push_browse.clicked.connect(lambda: self.browse_path(self.folder_path))
        self.flatfield_push_browse.clicked.connect(lambda: self.browse_path(self.flatfield_folder_path))
        flatfieldButton.clicked.connect(self.set_flatfield)
        
        #setup the signal to emit the directory path -> lambda just emits the custom signal (passing the value of the text line)
        self.folder_path.editingFinished.connect(lambda: self.update_dir.emit(self.folder_path.text()))
        self.flatfield_folder_path.editingFinished.connect(lambda: self.update_flatfield_dir.emit(self.flatfield_folder_path.text()))
        
        self.setLayout(folder_menu_layout)

    def browse_path(self, path_type: QLineEdit) -> None:
        """setups the file dialog to select a directory and sets the path_type to the selected directory

        Args:
            path_type (QLineEdit): QLineEdit whose text will be set to the selected directory
        """
        path = QFileDialog.getExistingDirectory(
        #path = getOpenFilesAndDirs(
            #parent=self,
            caption = "Select directory or singular .tif",
            directory = QDir().homePath(),
            options = QFileDialog.Option.DontUseNativeDialog
            #filter = "Directory or Tif Files (*.tif *.TIF *.dat *.DAT *.tiff)"
        )
        if path:
            path_type.setText(path)
            
    def set_flatfield(self) -> bool:
        self.flatfield_correction = not self.flatfield_correction
        self.flatfield_folder_path.setEnabled(self.flatfield_correction)
        self.flatfield_folder_path.setVisible(self.flatfield_correction)
        self.flatfield_push_browse.setVisible(self.flatfield_correction)
        self.flatfield_folder_path.setPlaceholderText("Select the folder containing the flatfield images")
        #flatfieldButton.setEnabled(self.flatfield_correction)
        #flatfield_push_browse.setEnabled(True)
        return self.flatfield_correction
            
    def get_folder(self):
        self.dir_path = self.folder_path.text()
        if not os.path.exists(self.dir_path):
            print("not a valid directory")
            sys.exit()
            
        #get data from directory
        # self.tifNames= []
        # self.dat = ""
        self.setTifNames = []
        
        for f in os.listdir(self.dir_path):
            if f.endswith('.TIF'):
                #print(f"tif: {f}")
                self.tifNames.append(f)
            if f.endswith('.DAT'):
                self.dat = f
            if f.endswith('.txt'):
                self.energies = f
        self.tifNames = sorted(self.tifNames)
        #####should we check data to make sure images match with number in .DAT??
        #if len(tif) > 0: blah blah blah
        self.tifNames.pop(0) #remove the first 0'th tif file which is just the sum of all
        
        
        if self.flatfield_correction:
            self.flatFieldDirPath = self.flatfield_folder_path.text()
            
            #print(self.flatfield_path is not None and not self.flatfield_path == "")
            #print(self.flatfield_correction)
        if (self.flatFieldDirPath is not "") and self.flatfield_correction:
            print("flatfield found")
            
            for f in os.listdir(self.flatfield_path):
                #print(f"files: {f}")
                if f.endswith('.TIF'):
                    #print(f"tif: {f}")
                    self.flatFieldNames.append(f)
                if f.endswith('.DAT'):
                    self.flatFieldDat = f
                if f.endswith('.txt'):
                    self.flatfield_energies = f
            self.flatFieldNames = sorted(self.flatFieldNames)
            if len(self.flatFieldNames) > 1:
                self.flatFieldNames.pop(0) #remove the first 0'th tif file which is just the sum of all
            #print(f"flatfield tif: {self.flatfield_tif}")
            
        '''we should keep in mind that not all may have a sum file, so we should check for that'''
        return self.dir_path, self.dat, self.tifNames
        
    def process_folder_data(self):
        self.setTiffArr(tiff_im(self.getDirPath(), self.getTifNames()))
        self.setFlatFieldArr(tiff_im(self.getFlatfieldDirPath, self.getFlatFieldNames()))
        
    # Converts all Tiff files in the form of an array
    def tiff_im(self, path, tif):
        """Based on the array of dir_tifs, generate all the necessary images into an array

        Args:
            path (String): dir_path to the base folder
            tif (Array or List): array/list of the names of the tif files

        Returns:
            tifIm: an array which contains 2d images, so a 3d dataset
        """
        tifIm = []
        for tiffName in tif: 
            tiffFile = Image.open(path + "/" + tiffName) #open the tiff file ###Todo may need to change '/' to os path thing
            imArray = np.array(tiffFile) #put the image into an array
            tifIm.append(imArray) #saves the tiff image array
        return tifIm
            
            
    # Gets the energies from the tiff files
    def get_energies_arr(self, path, dat): 
        df = pd(path + "/" + dat, header=None, names=['col'])
        energies = []
        num = ""
        for index, row in df.iterrows(): #this iterates through each row
            value = row['col'] #row['col'] is a string of each column
            
            for element in value: #this iterates through the string on that row
                
                if element.isnumeric() or element == ".": #this goes until we hit the numbers (aka tiff file numbers)
                    num = num + element #this will accumulate the numbers as long as the string element is numeric
                    
                else:
                    if not num=="": #if there were no numbers, reset num and break
                        energies.append(float(num)) #otherwise add it to the array
                        #print(array)
                    num = ""
                    break
                #print(array)
        lastNum = energies[-1] # this is the last number which will be the number of tiff files in the DAT
        self.energiesValArr = energies
        # print(f"energiesArr: {self.energiesValArr}")
        #print(lastNum)
        return energies

    #returns info from the dat file, FILE_ID, EXPERIMENT_NAME, MEASUREMENT_NAME, TIMESTAMP, INSTITUTION, SAMPLE
    def get_info(self, path, dat):
        df = pd(path + "/" + dat, header=None, names=['col'])
        info = df.head(9)
        # print(info)
        '''
        num = ""
        for index, row in df.iterrows(): #this iterates through each row
            value = row['col'] #row['col'] is a string of each column
            
            for element in value: #this iterates through the string on that row
                
                if element.isnumeric() or element == ".": #this goes until we hit the numbers (aka tiff file numbers)
                    num = num + element #this will accumulate the numbers as long as the string element is numeric
                    
                else:
                    if not num=="": #if there were no numbers, reset num and break
                        info.append(float(num)) #otherwise add it to the array
                        #print(array)
                    num = ""
                    break
                #print(array)
        lastNum = info[-1] # this is the last number which will be the number of tiff files in the DAT
        '''
        #print(lastNum)
        return info
    
    def setInfoFromDat(self, path, dat):
        # if self.dir_path == "":
            # return "No data path loaded"
        # self.infoFull = self.get_info(self.dir_path, self.dat) #first 9 lines
        try:
            df = pd(path + "/" + dat, header=None, names=['col'])
            self.infoFull = df.head(9)
        except:
            self.infoFull = "No Data Path Loaded... Failed"
                
        
    def setEnergies(self, energyArr):
        self.energiesValArr = energyArr
        
    def setTiffArr(self, tiffArr):
        self.tifArr = tiffArr
        
    def setTifNames(self, tifNames):
        self.tifNames = tifNames
    
    def setFlatFieldArr(self, flatfieldTiffArr):
        self.flatFieldArr = flatfieldTiffArr
        return self.flatFieldArr
      
    def getDatInfoFull(self):
        """Get the full dat info, currently first 9 lines

        Returns:
            _type_: _description_
        """
        return self.infoFull
        
    #get infohead
    def getDatInfoHeader(self):
        #print(f"infoHead: \n {infoHead}, \n {type(infoHead)}")
        #FILE_ID, EXPERIMENT_NAME, MEASUREMENT_NAME, TIMESTAMP, INSTITUTION, SAMPLE
        #columnsToInclude = ['FILE_ID*', 'EXPERIMENT_NAME*', 'MEASUREMENT_NAME*', 'TIMESTAMP*', 'INSTITUTION*', 'SAMPLE*']
        #self.infoStr = infoHead.apply(lambda row: row.astype(str).values, axis=1) #this is an ndArray
        #print(f"infoStr: \n {self.infoStr[0]}, \n {type(self.infoStr)}")
        
        # infoHead = self.getDatInfo()
        infoHead = self.getDatInfoFull()
        infoHead = infoHead.to_string(index=False, header=False)
        return infoHead
    
    def getEnergies(self):
        return self.energiesValArr
    
    def getTiffArr(self):
        return self.tifArr
    
    def getTifNames(self):
        return self.tifNames
    
    def getDirPath(self):
        return self.dir_path
    
    def getDatPath(self):
        return self.dat
    
    def getFlatfieldInfo(self):
        return self.flatFieldArr, self.flatFieldEnergiesArr
    
    def getFlatfieldDirPath(self):
        return self.flatFieldDirPath
    
    def getFlatFieldNames(self):
        return self.flatFieldNames
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Manager')
        
        self.file_widget = filesWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.file_widget)

        self.setLayout(layout)
        