"""
dialogs/save_dialog.py
----------
Custom dialogs like SaveModeDialog for encryption/plaintext selection.
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

class SaveModeDialog(QDialog):
    """Dialog to choose save mode (plaintext or encrypted) and set password."""
    def __init__(self, parent=None, crypto_available=True):
        super().__init__(parent)
        self.setWindowTitle("Save Mode")
        self.setFixedSize(350, 200)
        self.save_mode = None
        self.password = None

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("Choose how to save the file:"))

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter strong password (for encryption)")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setVisible(False)
        main_layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        self.plaintext_button = QPushButton("Plaintext (.txt)")
        self.encrypted_button = QPushButton("Encrypted (.txt.enc)")
        button_layout.addWidget(self.plaintext_button)
        button_layout.addWidget(self.encrypted_button)
        main_layout.addLayout(button_layout)

        self.plaintext_button.clicked.connect(self.select_plaintext)
        self.encrypted_button.clicked.connect(lambda: self.select_encrypted(crypto_available))
        self.password_input.textChanged.connect(self.check_password)

    def check_password(self):
        if self.save_mode == "encrypted":
            self.encrypted_button.setEnabled(bool(self.password_input.text().strip()))

    def select_plaintext(self):
        self.save_mode = "plaintext"
        self.password = None
        self.accept()

    def select_encrypted(self, crypto_available):
        if not crypto_available:
            QMessageBox.warning(self, "Error", "Cryptography library not installed!")
            return
        self.save_mode = "encrypted"
        self.password_input.setVisible(True)
        if self.password_input.text().strip():
            self.password = self.password_input.text()
            self.accept()
