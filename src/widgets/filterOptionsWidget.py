from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSlider, QPushButton, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal


class FilterOptionsWidget(QWidget):
    gaussianFilter = pyqtSignal(bool, float)  # Signal to emit filter settings
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        # Add filter options here, e.g., sliders, checkboxes, etc.
        # Example:
        
        self.initGaussianFilter()
        
        self.setLayout(self.layout)
        
    def initGaussianFilter(self):
        self.gaussian_label = QCheckBox("Gaussian Filter Sigma:")
        self.gaussian_label.setChecked(False)
        self.layout.addWidget(self.gaussian_label)
        self.gaussian_slider = QSlider(Qt.Orientation.Horizontal)
        self.gaussian_slider.setMinimum(0)
        self.gaussian_slider.setMaximum(100)
        self.gaussian_slider.setValue(0)
        self.gaussian_slider.setTickInterval(10)
        self.gaussian_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.gaussian_slider.valueChanged.connect(self.updateGaussianFilter)
        self.layout.addWidget(self.gaussian_slider)
        self.gaussianFilter.emit(False, 0.0)  # Initial state: no filter

    def updateGaussianFilter(self, value):
        self.gaussianFilter.emit(True, value / 50)  # Emit the filter settings
        
    def getGaussianToggle(self):
        return self.gaussian_label.isChecked()
    
    def getGaussianSigma(self):
        return self.gaussian_slider.value() / 50