from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QDialog
from PyQt6.QtCore import pyqtSignal

class ManualEnergyInputWidget(QDialog):
    energyValues = pyqtSignal(float, float, float)  # Signal to emit the list of energy values
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.start_energy_input = QLineEdit()
        self.end_energy_input = QLineEdit()
        self.spacing_input = QLineEdit()

        form_layout.addRow(QLabel("Starting Energy:"), self.start_energy_input)
        form_layout.addRow(QLabel("Ending Energy:"), self.end_energy_input)
        form_layout.addRow(QLabel("Spacing:"), self.spacing_input)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.on_submit)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(self.submit_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def on_submit(self):
        try:
            start = float(self.start_energy_input.text())
            end = float(self.end_energy_input.text())
            spacing = float(self.spacing_input.text())
            if spacing <= 0 or end <= start:
                # raise ValueError("Invalid range or spacing")
                QMessageBox.warning(self, "Invalid Input", "Please ensure that spacing is positive and end is greater than start.")
                return
            # QMessageBox.information(self, "Input Accepted",
                                    # f"Start: {start}\nEnd: {end}\nSpacing: {spacing}")
            # self.energyValues.emit(start, end, spacing)
            self.result = (start, end, spacing)
            # self.close()
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numeric values.")
            