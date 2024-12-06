import sys

sys.path.append("/Users/alexpoulin/Downloads/git/ARPES/src")

from tifConv import tiff_im
from os import listdir
from PIL import Image
import numpy as np

class tifStack():
    """_summary_
    Class to handle tif stack data. Its main purpose for this suite is to generate a tif stack. This is intended to be used in tomviz, to double check data vizualization.
    """
    def __init__(self, path, save_path):
        
        tif = []
        dat = ""
        
        for f in listdir(path):
            if f.endswith('.TIF'):
                #print(f"tif: {f}")
                tif.append(f)
            if f.endswith('.DAT'):
                dat = f
            if f.endswith('.txt'):
                energies = f
        tif = sorted(tif)
        #####should we check data to make sure images match with number in .DAT??
        #if len(tif) > 0: blah blah blah
        tif.pop(0) #remove the first 0'th tif file which is just the sum of all
        
        
        self.tifIm = tiff_im(path, tif)
        self.tif = tif
        self.path = path
        self.current = 0
        self.length = len(tif)
        self.save_path = save_path
        
        self.save_tif_stack2()
        
    def next(self):
        if self.current < self.length - 1:
            self.current += 1
        return self.tifIm[self.current]
    
    def prev(self):
        if self.current > 0:
            self.current -= 1
        return self.tifIm[self.current]
    
    def current(self):
        return self.tifIm[self.current]
    
    def get_current_name(self):
        return self.tif[self.current]
    
    def get_current_num(self):
        return self.current
    
    def get_length(self):
        return self.length
    
    def save_tif_stack(self):
        #tifstack = np.stack((self.tifIm[0], self.tifIm[1]))
        tifstack = np.stack(self.tifIm)
        '''
        for i in range(2, self.length):
            tifstack = np.concatenate((tifstack, self.tifIm[i]))
            '''
        print(f"tifstack type: {type(tifstack)}")
        print(f"tifstack shape: {tifstack.shape}")
        print(f"tifstack: {tifstack}")
        
        
        image_stack = Image.fromarray(tifstack)
        
        image_stack.save(self.save_path + "/tifStack.tif")
        
    def save_tif_stack2(self):
        image_list = []
        for posimage in self.tifIm:
            image_list.append(Image.fromarray(posimage))
        image_list[0].save(self.save_path + "/images.tiff", save_all=True, append_images=image_list[1:])


if __name__ == "__main__":
    save_path = '/Users/alexpoulin/Downloads'
    data_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/10.10.2024/ARPES_MnTe(exp30)_Ekinsweep_241010_175544/ARPES_MnTe(exp30)_Ekinsweep_241010_175545/Sum'
    stack = tifStack(data_path, save_path)
    
    
#/Users/alexpoulin/Downloads
#/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/07.17.2024/ARPES_MnTe_Direct_PE25_slit1p0_STIG0_240717_160232/ARPES_MnTe_Direct_slit1p0_FOV4p1_240717_160232/Sum