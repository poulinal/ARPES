import numpy as np
from PIL import Image

def tiffIm(path, tif):# Converts all Tiff files in the form of an array
    tifIm = []
    for tiffName in tif: 
        tiffFile = Image.open(path + "/" + tiffName) #open the tiff file
        imArray = np.array(tiffFile) #put the image into an array
        tifIm.append(imArray) #saves the tiff image array
    return tifIm