import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel

from src.arpesHome import ARPESHome
from src.energyVmomentum import EnergyVMomentum
from src.distributionCurve import DistCrve

class TabContent(QWidget):
    """Content class for each tab"""
    def __init__(self, tab_number):
        super().__init__()
        self.tab_number = tab_number
        
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add some content to demonstrate the tab
        # label = QLabel(f"This is Tab {self.tab_number}")
        # button = QPushButton(f"Button in Tab {self.tab_number}")
        # button.clicked.connect(lambda : print(f"Button clicked in tab {self.tab_number}"))
        
        # layout.addWidget(label)
        # layout.addWidget(button)
        self.setLayout(layout)

class ARPESMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_counter = 0
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("ARDA - Alexander Poulin")
        self.setGeometry(100, 100, 1024, 824)  # Window size
        
        # Create central widget and tab widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        self.arpesHome = ARPESHome()
        self.tab_widget.addTab(self.arpesHome, "ARPES Home")
        self.tab_counter = 1
        
        self.arpesHome.openEVM.connect(lambda resultData, energyArr, tifArr: self.open_evm(result=resultData, energyArr=energyArr, tifArr = tifArr))

        # # Create initial tab with the "Add Tab" button
        # self.create_main_tab()
        
    '''     
    # def create_main_tab(self):
    #     """Create the main tab with the 'Add Tab' button"""
    #     main_tab = QWidget()
    #     layout = QVBoxLayout(main_tab)
        
    #     add_tab_button = QPushButton("Add New Tab")
    #     add_tab_button.clicked.connect(self.add_new_tab)
        
    #     layout.addWidget(QLabel("Main Tab - Click button to add new tabs"))
    #     layout.addWidget(add_tab_button)
        
    #     self.tab_widget.addTab(main_tab, "Main")
    
    # def add_new_tab(self):
    #     """Add a new tab and switch to it"""
    #     # Create new tab content
    #     new_tab_content = TabContent(self.tab_counter)
        
    #     # Add tab to tab widget
    #     tab_index = self.tab_widget.addTab(new_tab_content, f"Tab {self.tab_counter}")
        
    #     # Switch to the new tab
    #     self.tab_widget.setCurrentIndex(tab_index)
        
    #     # Increment counter for next tab
    #     self.tab_counter += 1
    '''
        
    def open_evm(self, result, energyArr, tifArr):
        #Todo: make sure we actually need to pass everything other than result
        new_EVM_tab = EnergyVMomentum(results = result, energies = energyArr, tifArr = tifArr)
        
        tab_index = self.tab_widget.addTab(new_EVM_tab, f"EVM Tab {self.tab_counter}")
        
        self.tab_widget.setCurrentIndex(tab_index)
        
        self.tab_counter += 1
        
        new_EVM_tab.openMDC.connect(lambda resultData: self.open_distribution_curve("MDC", resultData))
        new_EVM_tab.openEDC.connect(lambda resultData: self.open_distribution_curve("EDC", resultData))
        
        # self.w = EnergyVMomentum(path = dirPath, dat = datPath, tifArr = tifData, result = result)
        #w.result = result
        # self.w.show()
        
    def open_distribution_curve(self, type, resultData):
        new_distr_tab = DistCrve(type, resultData)
        
        tab_index = self.tab_widget.addTab(new_distr_tab, f"DistrCurve Tab {self.tab_counter}")
        
        self.tab_widget.setCurrentIndex(tab_index)
        
        self.tab_counter += 1