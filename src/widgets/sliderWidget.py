from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QSlider
from PyQt6.QtCore import Qt


class EnergySliderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        
        layout = QVBoxLayout()

        self.setLayout(layout)
        
        #add slider to slide through images
        self.slider = QSlider(Qt.Orientation.Horizontal) #create new horizontal slider
        # if len(self.arpesDataObj.tif) <= 1:
        self.slider.setRange(0, 100)
        self.slider.setDisabled(True)
        # else:
        #     self.slider.setRange(0, len(self.tif) - 1)  # Set the range of the slider to the number of images
        
        
        layout.addWidget(self.slider, stretch=1)  # Add the slider to the layout with stretch=1 to make it take full width

            
    def enable(self, length):
        self.slider.setEnabled(True)
        self.slider.setRange(0, length)
        
    def getSlider(self):
        return self.slider