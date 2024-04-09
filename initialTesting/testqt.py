import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QVBoxLayout, QWidget, QSlider, QLayout as Qt
from PyQt6.QtGui import QPixmap

class RIXSGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DeLTA Lab ARPES GUI")
        #self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.setup_ui()

    def setup_ui(self):
        '''
        self.layout.addWidget(QLabel("Parameters"))

        parameters_layout = QVBoxLayout()
        valence_orbitals = QLineEdit()
        active_core = QLineEdit()
        valence_occupancy = QLineEdit()
        hunds = QLineEdit()
        jh = QLineEdit()
        spin_orbit_coupling = QLineEdit()
        parameters_layout.addWidget(valence_orbitals)
        parameters_layout.addWidget(active_core)
        parameters_layout.addWidget(valence_occupancy)
        parameters_layout.addWidget(hunds)
        parameters_layout.addWidget(jh)
        parameters_layout.addWidget(spin_orbit_coupling)

        self.layout.addLayout(parameters_layout)

        self.layout.addWidget(QLabel("X-Ray Transition"))

        xray_transition_layout = QVBoxLayout()
        atom_dropdown = QComboBox()
        atom_dropdown.addItems(["Option 1", "Option 2", "Option 3"])
        shell_dropdown = QComboBox()
        shell_dropdown.addItems(["Option 1", "Option 2", "Option 3"])
        xray_transition_layout.addWidget(atom_dropdown)
        xray_transition_layout.addWidget(shell_dropdown)

        self.layout.addLayout(xray_transition_layout)

        self.start_button = QPushButton("START RIXS")
        self.start_button.clicked.connect(self.send_rixs_command)
        self.layout.addWidget(self.start_button)

        self.layout.addWidget(QLabel("RIXS Output"))

        rixs_output_layout = QVBoxLayout()
        summary_label = QLabel("Summary of Slater integrals:")
        plot_label = QLabel("Plots:")
        self.checkbox = QPushButton("Export Chart")
        rixs_output_layout.addWidget(summary_label)
        rixs_output_layout.addWidget(plot_label)
        rixs_output_layout.addWidget(self.checkbox)

        self.layout.addLayout(rixs_output_layout)
        '''
        
        # Add image placeholder
        self.image_label = QLabel("Tif Image Placeholder")
        pixmap = QPixmap("For_Alex/Sum/Ag111-18-22eV-ARPES-scan_AV_056.TIF")  # Set your image path here
        self.image_label.setPixmap(pixmap)
        #self.setCentralWidget(self.image_label)
        
        self.image_label.setScaledContents(True)
        
        self.resize(int(pixmap.width() / 2), int(pixmap.height() / 2))
        
        
        self.layout.addWidget(self.image_label)
        
        # Add slider to slide through images
        self.slider = QSlider()
        self.slider = QSlider()
        #self.slider.setOrientation(Qt.Orientation.Horizontal)  # Set slider orientation to horizontal
        self.slider.setRange(0, 100)  # Set the range of the slider
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.layout.addWidget(self.slider, stretch=1)  # Add the slider to the layout with stretch=1 to make it take full width
        

    def send_rixs_command(self):
        print("START RIXS command sent")
        
    def slider_value_changed(self):
        print("Slider value changed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RIXSGUI()
    window.show()
    sys.exit(app.exec())
