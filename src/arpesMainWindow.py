import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel

from src.arpesHome import ARPESHome
from src.energyVmomentum import EnergyVMomentum
from src.distributionCurve import DistCrve
from src.widgets.advancedTabWidget import AdvancedTabWidget

from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtGui import QGuiApplication

class ARPESMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_counter = 0
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("ARDA - Alexander Poulin")
        # self.setGeometry(100, 100, 1024, 824)  # Window size
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, int(screen_geometry.width() * 0.6), screen_geometry.height() - 50)
        
        # Create central widget and tab widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = AdvancedTabWidget()
        layout.addWidget(self.tab_widget)
        
        self.arpesHome = ARPESHome()
        self.tab_widget.addTab(self.arpesHome, "ARPES Home")
        self.tab_counter = 1
        
        self.arpesHome.openEVM.connect(lambda resultData, energyArr, tifArr: self.open_evm(result=resultData, energyArr=energyArr, tifArr = tifArr))

        # # Create initial tab with the "Add Tab" button
        # self.create_main_tab()
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts for tab management"""
        
        # Ctrl+T to add new tab
        # new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        # new_tab_shortcut.activated.connect(self.add_new_tab)
        
        # Ctrl+W to close current tab
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(self.close_current_tab)
        
        # Ctrl+Shift+T to duplicate current tab
        duplicate_shortcut = QShortcut(QKeySequence("Ctrl+Shift+T"), self)
        duplicate_shortcut.activated.connect(self.duplicate_current_tab)
        
    
    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        self.tab_widget.close_tab(current_index)
    
    def duplicate_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        self.tab_widget.duplicate_tab(current_index)
        
    def open_evm(self, result, energyArr, tifArr):
        #Todo: make sure we actually need to pass everything other than result
        new_EVM_tab = EnergyVMomentum(results = result, energies = energyArr, tifArr = tifArr)
        
        tab_index = self.tab_widget.addTab(new_EVM_tab, f"EVM Tab {self.tab_counter}")
        
        self.tab_widget.setCurrentIndex(tab_index)
        
        self.tab_counter += 1
        
        new_EVM_tab.openMDC.connect(lambda resultData, extent: self.open_distribution_curve("MDC", resultData, extent))
        new_EVM_tab.openEDC.connect(lambda resultData, extent: self.open_distribution_curve("EDC", resultData, extent))
        
        # self.w = EnergyVMomentum(path = dirPath, dat = datPath, tifArr = tifData, result = result)
        #w.result = result
        # self.w.show()
        
    def open_distribution_curve(self, type, resultData, extent):
        new_distr_tab = DistCrve(type, resultData, extentSpace = extent)
        
        tab_index = self.tab_widget.addTab(new_distr_tab, f"DistrCurve Tab {self.tab_counter}")
        
        self.tab_widget.setCurrentIndex(tab_index)
        
        self.tab_counter += 1