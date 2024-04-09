### 2024 Alex Poulin

import sys
from PyQt6.QtWidgets import QApplication

from image import ARPESGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ARPESGUI()
    window.show()
    sys.exit(app.exec())