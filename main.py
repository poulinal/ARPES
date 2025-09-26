### 2024 Alex Poulin

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

import os

# print(os.getcwd())

main_dir = os.path.dirname(os.path.abspath(__file__))

from src.ArdaHomePage import HOMEGUI
# from src.arpesHome import ARPESHome

if __name__ == "__main__":
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

    app = QApplication(sys.argv)
    
    app.setPalette(palette)
    
    window = HOMEGUI(main_dir)
    window.show()
    
    try:
        # sys.exit(app.exec())
        exit_code = app.exec()
    except SystemExit:
        print("Closing Window (SystemExit)...")
    except KeyboardInterrupt:
        print("Force Closing Window (KeyboardInterrupt)...")
        exit_code = 0
    except:
        print("An unexpected error occurred.")
        exit_code = 1
    finally:
        app.quit()
        print("Application closed successfully.")
        sys.exit(exit_code)
        
    
    # sys.exit(app.exec())