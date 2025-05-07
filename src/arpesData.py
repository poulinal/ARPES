### 2025 Alexander Poulin
import numpy as np
from PyQt6.QtCore import QObject

class arpesData(QObject):
    def __init__(self, ):
        #setup class variables
        self.tifArr = np.zeros((50, 1024, 1024))
        self.dat = ""
        self.tif = ["dummy data"]
        self.energyArr = np.arange(0, 5, 0.1)
        self.energy = 0
        
    
    def getAllTifs(self):
        return self.tif
    
    def getCurrentTif(self, relEnergyIndex):
        return self.tif[relEnergyIndex]
    
    def getDat(self):
        return self.dat
    
    def getCurrentEnergy(self, relEnergyIndex):
        return self.energyArr[relEnergyIndex]
        
        
            
    def get_dir_data(self):
        self.files.get_folder()
        self.dir_path = self.files.dir_path
        self.dat = self.files.dat
        print(f"dir_path: {self.dir_path}")
        #self.energies = files.energies
        self.tif = self.files.tif
        self.tifArr = tiff_im(self.dir_path, self.tif)
        #self.tifArr = plt.tonemap(self.tifArr)
        
        if self.dat != "":
            self.energyArr = get_energies(self.dir_path, self.dat)
        
        arpesGraph.update_graph(self.getImage())
        self.slider.setEnabled(True)
        self.slider.setRange(0, len(self.tif) - 1)
        self.info.setText(self.get_info())
    
        
    def get_flatfield_data(self):
        self.files.get_folder()
        flatfield = self.files.flatfield_path
        if flatfield is not None:
            #print("doing flat field correction now")
            #print(f"before: {self.tifArr[0][0]}")
            flatfield_tif = self.files.flatfield_tif
            #print(f"flatfield from class: {self.files.flatfield_tif}")
            #print(f"flatfield: {flatfield_tif}")
            #print(f"flatfield path: {self.files.flatfield_path}")
            self.flatfield_arr = tiff_im(self.files.flatfield_path, flatfield_tif)
            #print(f"iris: {self.iris_flat_arr[0][0]}")
            #print(f"before: {self.tifArr}")
            if len(self.tifArr) != len(self.flatfield_arr):
                ff_index = 0
                for i in range(len(self.tifArr)):
                    if ff_index >= len(self.flatfield_arr):
                        ff_index = 0
                    self.tifArr[i] = np.divide(self.tifArr[i], self.flatfield_arr[ff_index])
                    ff_index += 1
            else:
                self.tifArr = np.divide(self.tifArr, self.flatfield_arr)
            #print(f"after: {self.tifArr}")
            #self.flatfield_dat = files.flatfield_dat
            #print(f"after: {self.tifArr[0][0]}")
            self.imageBuilder.build_image(self, self.getImage())
    
    