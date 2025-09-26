from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QFileDialog, QLineEdit)
from PyQt6.QtCore import QDir, pyqtSignal

class CustomFileDialog(QDialog):
    chosenPath = pyqtSignal(str, bool)  # Signal to emit chosen path and whether .dat file is present
    
    def __init__(self, directory=QDir().homePath(), parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Directory")
        self.directory = directory

        layout = QVBoxLayout()
        
        # Path display
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        layout.addWidget(self.path_edit)
        
        # Buttons
        btn_layout = QHBoxLayout()
        browse_btn = QPushButton("Browse Folder with .dat file (for energy)")
        custom_btn = QPushButton("Browse Folder and manually define energies")
        cancel_btn = QPushButton("Cancel")
        
        browse_btn.clicked.connect(self.browseWithDat)
        custom_btn.clicked.connect(self.browseWithoutDat)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(browse_btn)
        btn_layout.addWidget(custom_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.selected_directory = ""
    
    def browseWithDat(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", directory = self.directory)
        if directory:
            self.path_edit.setText(directory)
            self.selected_directory = directory
            
    
    def browseWithoutDat(self):
        print("Custom button clicked!")
        # Your custom logic here
    
    def get_directory(self):
        return self.selected_directory
