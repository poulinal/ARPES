import os, sys
from src.commonWidgets import get_folder

class files():
    def __init__(self):
        super().__init__()
        #get the directory path
        #'''
        self.dir_path = get_folder(self)
        if not os.path.exists(self.dir_path):
            print("not a valid directory")
            sys.exit()
            #'''
        #while testing:
        #self.dir_path = '/Users/alexpoulin/Downloads/git/ARPES/exData/Sum'
        #self.dir_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/ARPES_MnTe_Direct_CA1750_FOV5p4_PE25_240529_193451/ARPES_MnTe_Direct_CA1750_FOV5p4_PE25_240529_193451/Sum'
        #self.dir_path = '/Users/alexpoulin/Downloads/git/ARPES/Data from EQUAL/Kinetic_energy_mapping_MnTe_Se capped_240514_102635/MnTe (Se capped)_PEEM_Direct_240514_102635/Sum'
        #self.dir_path = '/Users/alexpoulin/Downloads/git/ARPES/Data from EQUAL/XPS data/Sum' #XPS data
        #self.dir_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/ARPES data 18th June24/ARPES_MnTe_Direct_Ekinsweep_240618_111423/ARPES_MnTe_Direct_FOV4p0_Iris_without large blisters_240618_111424/Sum'
        #self.dir_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/ARPES data 18th June24/ARPES_MnTe_Direct_with_large_blisters_Ekinsweep_240618_122202/ARPES_MnTe_Direct_FOV4p0_Iris_with large blisters_240618_122202/Sum'

        #get data from directory
        self.tif = []
        
        for f in os.listdir(self.dir_path):
            if f.endswith('.TIF'):
                #print(f)
                self.tif.append(f)
            if f.endswith('.DAT'):
                self.dat = f
            if f.endswith('.txt'):
                self.energies = f
        self.tif = sorted(self.tif)
        #####should we check data to make sure images match with number in .DAT??
        #if len(tif) > 0: blah blah blah
        self.tif.pop(0) #remove the first 0'th tif file which is just the sum of all
        '''we should keep in mind that not all may have a sum file, so we should check for that'''
        