import os, sys
from src.commonWidgets import get_folder

class files():
    def __init__(self):
        super().__init__()
        #get the directory path
        #'''
        self.dir_path, self.flatfield_path = get_folder(self)
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
        
        #self.dir_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/Arpes_MnTe_Direct_FOV4p0_20p7_iris_240618_175114/Sum'
        #self.iris_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/Arpes_MnTe_Direct_FOV4p0_20p7_iris_flat_240618_204621/Sum'
        
        #june 24 2024
        #self.dir_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/06.24.2024/ARPES_MnTe_Ekin_sweep_240624_145559/APES_MnTe_Direct_FOV41p8_PE25_S1p0_240624_145559/Sum'
        #self.iris_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/06.24.2024/ARPES_MnTe_Ekin_sweep_240624_145559/APES_MnTe_Direct_FOV41p8_PE25_S1p0_defocus_240625_010121/Sum'

        #june 20 2024
        #self.dir_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/06.20.2024/ARPES_MnTe_Direct_Ekinsweep_240620_151626/ARPES_MnTe_Direct_FOV4p0_240620_151626/Sum'
        #self.iris_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/06.20.2024/ARPES_MnTe_Direct_FOV4p0_flatfield_240621_120221/Sum'

        #june 18 2024
        #self.dir_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/ARPES data 18th June24/ARPES_MnTe_Direct_with_large_blisters_Ekinsweep_240618_122202/ARPES_MnTe_Direct_FOV4p0_Iris_with large blisters_240618_122202/Sum'
        #self.iris_path = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/ARPES data 18th June24/ARPES_MnTe_Direct_Ekinsweep_240618_111423/ARPES_MnTe_Direct_FOV4p0_Iris_without large blisters_240618_111424/Sum'
        
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
        
        if self.flatfield_path is not None:
            print("flatfield found")
            #self.iris_path = self.dir_path.split("iris")[0] + "iris_flat" + self.dir_path.split("iris")[1]
            #print(self.flatfield_path)
            
            self.flatfield_tif = []
            for f in os.listdir(self.flatfield_path):
                if f.endswith('.TIF'):
                    self.flatfield_tif.append(f)
                if f.endswith('.DAT'):
                    self.flatfield_dat = f
                if f.endswith('.txt'):
                    self.flatfield_energies = f
            #self.iris_flat_dat = '/Users/alexpoulin/Library/CloudStorage/OneDrive-NortheasternUniversity/DeLTA Lab/data/Arpes_MnTe_Direct_FOV4p0_20p7_iris_flat_240618_204621/Sum'
            self.flatfield_tif = sorted(self.flatfield_tif)
            #####should we check data to make sure images match with number in .DAT??
            #if len(tif) > 0: blah blah blah
            self.flatfield_tif.pop(0) #remove the first 0'th tif file which is just the sum of all
            
        '''we should keep in mind that not all may have a sum file, so we should check for that'''
        