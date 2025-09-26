### 2024 Alex Poulin
import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QPushButton, QDialog, QDialogButtonBox, QLabel, QCheckBox

class CustomFileDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a custom button
        self.custom_button = QCheckBox("Include Flat Field Correction")
        self.custom_button.setCheckable(True)

        # Create a label to show toggle state
        #self.toggle_label = QLabel("Toggle is OFF")

        # Create a layout for the custom widget
        custom_layout = QVBoxLayout()
        #custom_layout.addWidget(self.toggle_label)
        custom_layout.addWidget(self.custom_button)

        # Add the custom layout to the file dialog
        #custom_widget = self.layout().itemAt(self.layout().count() - 1).widget()
        file_dialog = QFileDialog()
        custom_widget = file_dialog.layout().addWidget(self.custom_button)
        custom_widget.setLayout(custom_layout)

    def on_toggle(self, checked):
        if checked:
            self.toggle_label.setText("Toggle is ON")
        else:
            self.toggle_label.setText("Toggle is OFF")

class QFileDialogFlatFieldWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        open_button = QPushButton("Open File Dialog", self)
        open_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(open_button)

        self.setLayout(layout)
        self.setWindowTitle('Custom File Dialog Example')
        self.show()

    def open_file_dialog(self):
        dialog = CustomFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            print(f'Selected file: {dialog.selectedFiles()[0]}')
            print(f'Toggle state: {dialog.custom_button.isChecked()}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QFileDialogFlatFieldWidget()
    sys.exit(app.exec())
