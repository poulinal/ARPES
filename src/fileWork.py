import os, sys

from PyQt6.QtWidgets import QFileDialog, QDialogButtonBox, QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QHBoxLayout, QGroupBox, QFileDialog, QWidget
from PyQt6.QtCore import QDir, pyqtSignal

from src.widgets.getfileordir import getOpenFilesAndDirs

class files(QWidget):
    
    update_dir = pyqtSignal(str)
    update_flatfield_dir = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        #get the directory path
        #'''
        self.setupWidget()
        
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
            #'''
        #while testing:
        #self.dir_path = '/Users/alexpoulin/Downloads/git/ARPES/exData/Sum'
        #self.dir_path = '/Users/alexpoulin/Downloads/git/ARPES/Data from EQUAL/XPS data/Sum' #XPS data
        
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
        self.dat = ""
        
        for f in os.listdir(self.dir_path):
            if f.endswith('.TIF'):
                #print(f"tif: {f}")
                self.tif.append(f)
            if f.endswith('.DAT'):
                self.dat = f
            if f.endswith('.txt'):
                self.energies = f
        self.tif = sorted(self.tif)
        #####should we check data to make sure images match with number in .DAT??
        #if len(tif) > 0: blah blah blah
        self.tif.pop(0) #remove the first 0'th tif file which is just the sum of all
        
        
        self.flatfield_path = None
        if self.flatfield_correction:
            self.flatfield_path = self.flatfield_folder_path.text()
            
            #print(self.flatfield_path is not None and not self.flatfield_path == "")
            #print(self.flatfield_correction)
        if (self.flatfield_path is not None and not self.flatfield_path == "") and self.flatfield_correction:
            print("flatfield found")
            
            self.flatfield_tif = []
            for f in os.listdir(self.flatfield_path):
                #print(f"files: {f}")
                if f.endswith('.TIF'):
                    #print(f"tif: {f}")
                    self.flatfield_tif.append(f)
                if f.endswith('.DAT'):
                    self.flatfield_dat = f
                if f.endswith('.txt'):
                    self.flatfield_energies = f
            self.flatfield_tif = sorted(self.flatfield_tif)
            if len(self.flatfield_tif) > 1:
                self.flatfield_tif.pop(0) #remove the first 0'th tif file which is just the sum of all
            #print(f"flatfield tif: {self.flatfield_tif}")
            
        '''we should keep in mind that not all may have a sum file, so we should check for that'''
        
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Manager')
        
        self.file_widget = files()

        layout = QVBoxLayout()
        layout.addWidget(self.file_widget)

        self.setLayout(layout)
        