### 2024 Alex Poulin
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class cutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.canvas = canvas  # Reference to the Matplotlib canvas

        # Create layout for the toolbar
        self.layout = QHBoxLayout(self)
        
        # Create buttons
        self.cut_button = QPushButton("Zoom")
        
        # Add buttons to the layout
        self.layout.addWidget(self.cut_button)
        self.cut_button.clicked.connect(self.activate_cut)

    def activate_cut(self):
        print("cut")
        #self.canvas.mpl_connect('button_press_event', self.canvas.figure.gca().zoom)  # Connect zoom action
        #self.canvas.toolbar.zoom()  # Activate Matplotlib's built-in zoom mode