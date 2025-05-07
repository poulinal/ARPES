### 2024 Alex Poulin

import sys
from PyQt6.QtWidgets import QApplication

import os

print(os.getcwd())

from src.ArdaHomePage import HOMEGUI
# from src.arpesHome import ARPESHome

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HOMEGUI()
    window.show()
    sys.exit(app.exec())