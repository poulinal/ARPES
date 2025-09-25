### 2025 Alexander Poulin
import numpy as np
from PyQt6.QtCore import QObject

from src.tifConv import tiff_im, get_energies
from src.widgets.arpesGraph import arpesGraph

from scipy.ndimage import gaussian_filter

class arpesData(QObject):
    def __init__(self, ):
        #setup class variables
        self.tifArr = np.zeros((50, 1024, 1024))
        # self.dat = ""
        # self.tifFileArr = ["dummy data"]
        self.energyArr = np.arange(0, 5, 0.1)
        self.energy = 0
        
        self.flatFieldArr = None
        self.flatFieldEnergyArr = None
        
    
    def getAllTifFiles(self):
        return self.tifArr
    
    def getCurrentTif(self, applyGaussian = False, sigma = 1.5):
        # print(f"currentTif self.energy: {self.energy}")
        # print(f"currentTif current TifArr: {self.tifArr}")
        if applyGaussian:
            return gaussian_filter(self.tifArr[self.energy], sigma = sigma)
        else:
            return self.tifArr[self.energy]
    
    def getCurrentEnergy(self):
        # print(f"size: {len(self.energyArr)} with energy: {self.energy}")
        try:
            return self.energyArr[self.energy], self.energy
        except RuntimeError as e:
            print(f"ERROR in getCurrentEnergy: size: {len(self.energyArr)} with energy: {self.energy}")
            print(f"runtime error: {e}, where energy: {self.energy} and energyArr: {self.energyArr}")
            return RuntimeError(e)
            
    
    def getTifData(self):
        return self.tifArr
    
    
    def setCurrentEnergy(self, energy):
        """Set the index of the current energy, i.e. we will use this value to index the energyArray to get the actual raw energy

        Args:
            energy (int): integer index value that is between 0 and len(self.energyArr)
        """
        # print(f"setting current energy: energy: {energy}, arr: {len(self.energyArr)}")
        self.energy = energy if energy <= len(self.energyArr) - 1 and energy >= 0 else RuntimeError("Set energy must be between 0 and len(self.energyArr) - 1")
        
    def setEnergyArr(self, energyArr):
        self.energyArr = energyArr
    
    def getEnergyArr(self):
        """Get the energy array

        Returns:
            np.array: energy array
        """
        return self.energyArr
    
    
    def setTifArr(self, tifArr):
        # print(f"setTifArr: len(tifArr) = {len(tifArr)}")
        self.tifArr = tifArr
        return self.tifArr
        
        
    def get_flatfield_data(self, flatfieldArr):
        self.flatFieldArr = flatfieldArr
        print(f"len(self.flatFieldArr) = {len(self.flatFieldArr)}")
        print(f"len(self.tifArr) = {len(self.tifArr)}")
        if self.flatFieldArr is not None and len(self.flatFieldArr) > 0:
            print(f"len(self.flatFieldArr) = {len(self.flatFieldArr)}")
            if len(self.tifArr) != len(self.flatFieldArr):
                ff_index = 0
                for i in range(len(self.tifArr)):
                    if ff_index >= len(self.flatFieldArr):
                        ff_index = 0
                    self.tifArr[i] = np.divide(self.tifArr[i], self.flatFieldArr[ff_index])
                    ff_index += 1
            else:
                self.tifArr = np.divide(self.tifArr, self.flatFieldArr)

            # self.imageBuilder.build_image(self, self.getImage())
    
    
    #interpolate the line to go across the image
    def interpl(self, startx, starty, lastx, lasty, posExtended, distance = None, vmin = None, vmax = None): 
        if (lastx is None or lasty is None or startx is None or starty is None):
            return
        
        # print(f"posExtended: {posExtended}")
        #print the start and end points for posExtended
        print(f"start and end for posExtended: {posExtended[0][0]}, {posExtended[1][0]} and {posExtended[0][-1]}, {posExtended[1][-1]}")
        if (posExtended[0] is None or posExtended[1] is None):
            return #make sure there is a line to interpolate
        
        #maybe add some checks here to dumbproof
        
        #only return those points in the array which align with x_new and y_new
        #result = np.zeros(shape = (len(posExtended[0]), len(posExtended[1]))) #this will eventually be converted to image so should be height by width (height is number of images, width is distance of selection)
        #result = np.zeros(shape = (int(len(self.tifArr)), int(distance)))
        print(distance)
        resultColLength = int(distance)
        resultRowLength = int(len(self.tifArr))
        result = np.zeros(shape = (resultRowLength, resultColLength)) #note shape is row, col
        
        queryXindexes = np.linspace(posExtended[0][0], posExtended[0][-1], resultColLength, endpoint=False)
        
        print(f"queryXindexes: {queryXindexes}, length: {len((queryXindexes))}")
        
        imIndex = 0
        print(f"posExtended: {posExtended}, posExtended[0] shape: {posExtended[0].shape}, posExtended[1] shape: {posExtended[1].shape}")
        for tiffIm in self.tifArr:
            for index, indexValue in enumerate(queryXindexes):
                #data point on the exact point (note posExtended[0] is x coordinates along line, posExtended[1] is y coordinates along line)
                # print(f"index: {index}, indexValue: {indexValue}")
                nearestXPix = int(posExtended[0][int(index)])
                nearestYPix = int(posExtended[1][int(index)])
                # print(f"nearestXPix: {nearestXPix}, nearestYPix: {nearestYPix}")
                
                #gamma = self.distanceWeightedAverage(nearestXPix, nearestYPix, posExtended[0], posExtended[1], 2)
                #dataPoint = gamma * tiffIm[nearestXPix][nearestYPix]
                
                dataPoint = tiffIm[nearestXPix][nearestYPix]
                #dataPoint = self.distanceWeightedAverage(nearestXPix, nearestYPix, posExtended[0][i], posExtended[1][i], 2) * tiffIm[nearestXPix][nearestYPix]
                
                #posExtended[0][i] gets the xpoint on that iteration
                
                cluster_data = 1 #amount of points we cluster --for average later
                #if (posExtended[0][i] < 0 or posExtended[0][i] >= 1024 or posExtended[1][i] < 0 or posExtended[1][i] >= 1024):
                #dataPoint += tiff_im[int(posExtended[0][i])][int(posExtended[1][i])]
                
                
                if (nearestXPix > 0): #can go to left for cluster
                    dataPoint += tiffIm[nearestXPix - 1][nearestYPix]
                    #dataPoint += self.distanceWeightedAverage(nearestXPix - 1, nearestYPix, posExtended[0][i], posExtended[1][i], 2) * tiffIm[nearestXPix - 1][nearestYPix]
                    cluster_data += 1
                    
                    #diagonal left up and down
                    if (nearestYPix > 0): #can go to up for cluster
                        dataPoint += tiffIm[nearestXPix - 1][nearestYPix - 1]
                        cluster_data += 1
                        #dataPoint += self.distanceWeightedAverage(nearestXPix - 1, nearestYPix - 1, posExtended[0][i], posExtended[1][i], 2) * tiffIm[nearestXPix - 1][nearestYPix - 1]
                    if (nearestYPix < self.tifArr[0].shape[0] - 1): #can go to down for cluster
                        dataPoint += tiffIm[nearestXPix - 1][nearestYPix + 1]
                        cluster_data += 1
                        #dataPoint += self.distanceWeightedAverage(nearestXPix - 1, nearestYPix + 1, posExtended[0][i], posExtended[1][i], 2) * tiffIm[nearestXPix - 1][nearestYPix + 1]
                    
                if (nearestXPix < self.tifArr[0].shape[1] - 1): #can go to right for cluster
                    dataPoint += tiffIm[nearestXPix + 1][nearestYPix]
                    cluster_data += 1
                    #dataPoint += self.distanceWeightedAverage(nearestXPix + 1, nearestYPix, posExtended[0][i], posExtended[1][i], 2) * tiffIm[nearestXPix + 1][nearestYPix]
                    
                    #diagonal right up and down
                    if (nearestYPix > 0): #can go to up for cluster
                        dataPoint += tiffIm[nearestXPix + 1][nearestYPix - 1]
                        cluster_data += 1
                        #dataPoint += self.distanceWeightedAverage(nearestXPix + 1, nearestYPix - 1, posExtended[0][i], posExtended[1][i], 2) * tiffIm[nearestXPix + 1][nearestYPix - 1]
                    if (nearestYPix < self.tifArr[0].shape[0] - 1): #can go to down for cluster
                        dataPoint += tiffIm[nearestXPix + 1][nearestYPix + 1]
                        cluster_data += 1
                        #dataPoint += self.distanceWeightedAverage(nearestXPix + 1, nearestYPix + 1, posExtended[0][i], posExtended[1][i], 2) * tiffIm[nearestXPix + 1][nearestYPix + 1]
                    
                if (nearestYPix > 0): #can go to up for cluster
                    dataPoint += tiffIm[nearestXPix][nearestYPix - 1]
                    cluster_data += 1
                    #dataPoint += self.distanceWeightedAverage(nearestXPix, nearestYPix - 1, posExtended[0][i], posExtended[1][i], 2) * tiffIm[nearestXPix][nearestYPix - 1]
                
                if (nearestYPix < self.tifArr[0].shape[0] - 1): #can go to down for cluster
                    dataPoint += tiffIm[nearestXPix][nearestYPix + 1]
                    cluster_data += 1
                    #dataPoint += self.distanceWeightedAverage(nearestXPix, nearestYPix + 1, posExtended[0][i], posExtended[1][i], 2) * tiffIm[nearestXPix][nearestYPix + 1]
                # print(f"clusterdata: {cluster_data}")
                if cluster_data > 1:
                    dataPointAvg = dataPoint / cluster_data
                
                
                ###Todo finish clipping, currently zeros everything
                # if vmin is not None and vmax is not None:
                #     print(f"datapoint before clip: {dataPointAvg}")
                #     #dataPoint = (dataPoint - self.vmin) / (self.vmax - self.vmin)
                #     dataPointAvg = np.clip(dataPointAvg, vmin, vmax)
                #     print(f"new datapoint: {dataPointAvg}")
                # print(f"dataPointAvg: {dataPointAvg}")
                
                result[imIndex][int(index)] = dataPointAvg
                # end of for loop i (across image) iteration
            imIndex += 1
            #end of for loop for i (across image)
        #end of for loop for tiffIm
            
        result = result.astype(float)
        #print(result)
        result = np.flip(result, axis=0)
        # print(f"nonzero result in interpl: {np.count_nonzero(result)}")
        # self.show_new_image(result)
        return result
    
    
    def distanceWeightedAverage(self, x, y, x_new, y_new, p):
        ### p is the power of the distance
        ### x and y are the coordinates of the point we are trying to find the value of
        ### x_new and y_new are the coordinates of the point we are trying to find the value of
        ### returns the weighted average of the point
        gamma = 0
        for i in range(len(x_new)):
            gamma += (1 / (np.sqrt((x_new[i] - x)**2 + (y_new[i] - y)**2))**p)
        return gamma