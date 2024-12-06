### 2024 Alex Poulin
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from src.widgets.cutWidget import cutWidget


class matplotToolbar(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas  # Reference to the Matplotlib canvas

        # Create layout for the toolbar
        self.layout = QHBoxLayout(self)
        
        # Create buttons
        self.zoom_button = QPushButton("Zoom")
        self.pan_button = QPushButton("Pan")
        self.reset_button = QPushButton("Reset")
        
        self.navbar = NavigationToolbar(self.canvas, self)
        self.navbar.addWidget(cutWidget())

        # Add buttons to the layout
        self.layout.addWidget(self.navbar)
        '''
        self.layout.addWidget(self.zoom_button)
        self.layout.addWidget(self.pan_button)
        self.layout.addWidget(self.reset_button)
        
        # Connect buttons to their functions
        self.zoom_button.clicked.connect(self.activate_zoom)
        self.pan_button.clicked.connect(self.activate_pan)
        self.reset_button.clicked.connect(self.reset_view)
        

    def activate_zoom(self):
        self.canvas.mpl_connect('button_press_event', self.canvas.figure.gca().zoom)  # Connect zoom action
        self.canvas.toolbar.zoom()  # Activate Matplotlib's built-in zoom mode

    def activate_pan(self):
        self.canvas.toolbar.pan()  # Activate Matplotlib's built-in pan mode

    def reset_view(self):
        self.canvas.figure.gca().autoscale()  # Reset to original view
        self.canvas.draw()  # Redraw the canvas
        
        '''