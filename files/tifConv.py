import numpy as np
from PIL import Image

def tiffIm(path, tif):# Converts all Tiff files in the form of an array
    tifIm = []
    for tiffName in tif: 
        tiffFile = Image.open(path + "/" + tiffName) #open the tiff file
        imArray = np.array(tiffFile) #put the image into an array
        tifIm.append(imArray) #saves the tiff image array
    return tifIm


def getEnergies(path, tif): # Gets the energies from the tiff files
    energies = []
    for tiffName in tif:
        tiffFile = Image.open(path + "/" + tiffName) #open the tiff file
        energies.append(tiffFile.tag_v2[0x1429][0]) #gets the energy from the tiff file
    return energies