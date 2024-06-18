### 2024 Alex Poulin

import sys
from PyQt6.QtWidgets import QApplication

from src.homePage import HOMEGUI
from src.image import ARPESGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HOMEGUI()
    window.show()
    sys.exit(app.exec())