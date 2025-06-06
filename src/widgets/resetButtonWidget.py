### Alexander Poulin 2025

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class ResetButton(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.setLayout(layout)
        
        
         # Create a square button
        self.resetButton = QPushButton("Reset Line")
        self.resetButton.setFixedSize(100, 25)  # Set the fixed size of the button to create a square shape
        # self.resetButton.clicked.connect(self.reset_line)
        #self.resetButton.hide()
        self.resetButton.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")
        
    def getButton(self):
        return self.resetButton
    
    def disable(self):
        #self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
        self.resetButton.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")
        self.resetButton.hide()
        
    def enable(self):
        pass