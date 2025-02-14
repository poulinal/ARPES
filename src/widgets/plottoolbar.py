### 2024 Alex Poulin
from PyQt6.QtWidgets import QWidget, QCheckBox, QComboBox
from PyQt6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#import os 
  



class matplotToolbar(NavigationToolbar):
    def __init__(self, canvas, parent=None):
        super(matplotToolbar, self).__init__(canvas, parent)

        # Add "Graph Typ e" drop-down menu
        graph_types = ["Line Graph", "Bar Chart", "Scatter Plot"]
        #'''
        self.cut_checkbox = QCheckBox(self)
        self.cut_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
            }
            QCheckBox::indicator:unchecked {
                image: url("src/images/layers (2).png");
            }
            QCheckBox::indicator:checked {
                image: url("src/images/layers (3).png");
            }
        """)
        
        #set the cut_checkbox to a custom image of a scissor
        #self.cut_checkbox.setIcon(QIcon("ARPES/src/images/scissors.png"))
        self.addWidget(self.cut_checkbox)
        '''
        self.graph_type_combobox = QComboBox(self)
        self.graph_type_combobox.addItems(graph_types)
        self.graph_type_combobox.currentIndexChanged.connect(self._on_graph_type_selected)
        self.addWidget(self.graph_type_combobox)
        '''
    '''
    def _on_graph_type_selected(self):
        # Create a new graph based on the selected type from the drop-down menu
        graph_type = self.graph_type_combobox.currentText()
        fig = self.canvas.figure
        n_plots = len(fig.get_axes())
 
        for ax in fig.get_axes():
            ax.remove()
 
        # Set the subplot grid to 1 row and 1 column
        n_new_rows, n_new_cols = 1, 1
 
        if graph_type == "Line Graph":
            new_ax = fig.add_subplot(n_new_rows, n_new_cols, 1)
            new_ax.plot([1, 2, 3], [4, 2, 6], color='blue')  # Set color to blue
            new_ax.set_title('Line Graph')
 
        elif graph_type == "Bar Chart":
            new_ax = fig.add_subplot(n_new_rows, n_new_cols, 1)
            bars = new_ax.bar(['A', 'B', 'C'], [3, 7, 2], color=['red', 'green', 'blue'])  # Set colors to red, green, and blue
            new_ax.set_title('Bar Chart')
 
        elif graph_type == "Scatter Plot":
            new_ax = fig.add_subplot(n_new_rows, n_new_cols, 1)
            new_ax.scatter([1, 2, 3], [4, 2, 6], color='orange')  # Set color to orange
            new_ax.set_title('Scatter Plot')
 
        fig.canvas.draw()
        #'''