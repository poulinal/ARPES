### 2024 Alex Poulin

import numpy as np
from PIL import Image
from pandas import read_csv as pd

# Converts all Tiff files in the form of an array
def tiff_im(path, tif):
    # print(f"tiff_im, tifnames: {tif}")
    tifIm = []
    for i, tiffName in enumerate(tif): 
        tiffFile = Image.open(path + "/" + tiffName) #open the tiff file
        
        # print(f"tiff_im, tiffFile: {tiffFile, i}")
        imArray = np.array(tiffFile) #put the image into an array
        # print(f"tiff_im, imArray nonzero: {np.nonzero(imArray)}")
        tifIm.append(imArray) #saves the tiff image array
    # print(f"tiff_im, tifIm: {tifIm}")
    return tifIm

# Gets the energies from the tiff files
def get_energies(path, dat): 
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
    #print(lastNum)
    return energies

#returns info from the dat file, FILE_ID, EXPERIMENT_NAME, MEASUREMENT_NAME, TIMESTAMP, INSTITUTION, SAMPLE
def get_info(path, dat):
    df = pd(path + "/" + dat, header=None, names=['col'])
    info = df.head(9)
    print(info)
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
