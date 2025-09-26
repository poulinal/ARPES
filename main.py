### 2024 Alex Poulin

import sys
from PyQt6.QtWidgets import QApplication

import os

# print(os.getcwd())

main_dir = os.path.dirname(os.path.abspath(__file__))

from src.ArdaHomePage import HOMEGUI
# from src.arpesHome import ARPESHome

if __name__ == "__main__":
    app = QApplication(sys.argv)
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