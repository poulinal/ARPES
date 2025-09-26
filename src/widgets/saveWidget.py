#Alexander Poulin 2025

##allow for saving of raw data, graph, or video

import os, sys

from PyQt6.QtWidgets import QFileDialog, QDialogButtonBox, QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QHBoxLayout, QGroupBox, QFileDialog, QWidget
from PyQt6.QtCore import QDir, pyqtSignal

import numpy as np

class saveWidget(QWidget):
    def __init__(self):
        pass