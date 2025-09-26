### 2024 Alex Poulin
from PyQt6.QtWidgets import QWidget, QCheckBox, QComboBox, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#import os 
  
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                            QWidget, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction

class CustomToolbar(NavigationToolbar):
    lineCutModeToggled = pyqtSignal(bool)
    segLineCutModeToggled = pyqtSignal(bool)
    boxCutModeToggled = pyqtSignal(bool)
    resetButtonClicked = pyqtSignal()
    exportData = pyqtSignal()
    
    
    
    def __init__(self, canvas, parent=None):
        super().__init__(canvas, parent)
        self.canvas = canvas
        
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # self.setMinimumWidth(100)  # Set a reasonable minimum width
    
        # Add separator before custom buttons
        self.addSeparator()
        
        # Add custom buttons
        self.add_custom_actions()
    
    def add_custom_actions(self):
        """Add custom buttons to the toolbar"""
        
        # Get the default actions before clearing
        default_actions = self.actions().copy()
        # Clear all actions
        self.clear()
        
        # Add back the default actions (excluding the last separator if any)
        # for action in default_actions:
        for i in range(len(default_actions)):
            action = default_actions[i]
            # Only add actions except the very last one
            if i < len(default_actions) - 2:
                # okay so len(default_actions) - 1 is the normal behavior. However the original toolbar has an extra separator at the end for some reason which kept custom buttons to being forced into the overflow menu. So I skip the last action instead of adding all of them (including the end spacer).
                # print(f"Re-adding action: {action.text()}")
                self.addAction(action)
        # Add separator after default actions
        self.addSeparator()
        
        
    def add_lincut_button(self):
        """Add Line Cut button to the toolbar"""
        self.linCutAction = QAction("Line Cut", self)
        self.linCutAction.setToolTip("Create Line Cut Across Data")
        self.linCutAction.setCheckable(True)
        self.linCutAction.triggered.connect(self.toggle_line_cut_mode)
        self.addAction(self.linCutAction)
        
    def add_seg_lincut_button(self):
        """Add Segmented Line Cut button to the toolbar"""
        self.segLinCutAction = QAction("Seg Line Cut", self)
        self.segLinCutAction.setToolTip("Segmented Line Cut")
        self.segLinCutAction.setCheckable(True)
        self.segLinCutAction.triggered.connect(self.toggle_seg_line_cut_mode)
        self.addAction(self.segLinCutAction)
        
    def add_boxcut_button(self):
        """Add Box Cut button to the toolbar"""
        self.boxCutAction = QAction("Box Cut", self)
        self.boxCutAction.setToolTip("Create Box Cut Across Data")
        self.boxCutAction.setCheckable(True)
        self.boxCutAction.triggered.connect(self.toggle_box_cut_mode)
        self.addAction(self.boxCutAction)
    
    def add_reset_button(self):
        """Add Reset button to the toolbar"""
        reset_action = QAction("Reset", self)
        reset_action.setToolTip("Reset plot to default view")
        reset_action.triggered.connect(self.reset_plot)
        self.addAction(reset_action)
        self.addSeparator()
        
    def reset_plot(self):
        """Reset plot to original state"""
        # self.canvas.reset_plot()
        # QMessageBox.information(self, "Reset", "To be Implemented...")
        self.resetButtonClicked.emit()
    
    def export_data(self):
        """Export current plot data to CSV"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "", "CSV Files (*.csv)")
        
        if filename:
            # self.canvas.export_data(filename)
            self.exportData.emit()
            # QMessageBox.information(self, "Export", f"Data exported to {filename}")
    
    def toggle_grid(self, checked):
        """Toggle grid display"""
        for ax in self.canvas.figure.get_axes():
            ax.grid(checked)
        self.canvas.draw()
    
    def toggle_log_scale(self, checked):
        """Toggle Y-axis log scale"""
        for ax in self.canvas.figure.get_axes():
            if checked:
                ax.set_yscale('log')
            else:
                ax.set_yscale('linear')
        self.canvas.draw()
        
    def toggle_line_cut_mode(self, checked):
        # print(f"toggle_line_cut_mode: {checked}")
        self.linCutAction.setChecked(checked)
        self.lineCutModeToggled.emit(checked)
        
    def toggle_seg_line_cut_mode(self, checked):
        # print(f"toggle_seg_line_cut_mode: {checked}")
        self.segLinCutAction.setChecked(checked)
        self.segLineCutModeToggled.emit(checked)
        
    def toggle_box_cut_mode(self, checked):
        self.boxCutAction.setChecked(checked)
        self.boxCutModeToggled.emit(checked)