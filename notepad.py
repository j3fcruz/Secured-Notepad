"""
notepad.py
----------
Main window for Secured Notepad. Integrates editor, encryption, dialogs, and themes.
"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QStatusBar, QAction, QFileDialog,
    QMessageBox, QInputDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QFile, QTextStream
from modules.editor import EnhancedTextEditor
from modules.encryption_cpp import encrypt_data, decrypt_data, CRYPTO_AVAILABLE
from modules.dialogs import SaveModeDialog

class EnhancedNotepad(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- State Variables ---
        self.current_file = None
        self.is_encrypted = False

        # --- Window Setup ---
        self.setWindowTitle("Untitled - Secured Notepad")
        self.setGeometry(100, 100, 1000, 700)
        #self.setWindowIcon(QIcon(ICON_PATH))

        # --- Editor Setup ---
        self.text_editor = EnhancedTextEditor()
        self.text_editor.document().setModified(False)
        self.setCentralWidget(self.text_editor)

        # Connect editor signals
        self.text_editor.cursorPositionChanged.connect(self.update_status_bar)
        self.text_editor.textChanged.connect(self.update_status_bar)

        # --- Status Bar ---
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Permanent widgets
        self.line_col_label = QLabel("Ln 1, Col 1")
        self.char_count_label = QLabel("Length: 0")
        self.encoding_label = QLabel("UTF-8")
        self.crypto_status_label = QLabel("Plaintext")
        self.crlf_label = QLabel("CRLF")
        self.zoom_label = QLabel("Zoom: 100%")

        self.statusBar.addPermanentWidget(self.line_col_label)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(self.char_count_label)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(self.encoding_label)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(self.crypto_status_label)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(self.crlf_label)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(self.zoom_label)

        self.update_status_bar()

        # --- Menu ---
        self.init_menu()

    # ---------------- Status Bar ----------------
    def update_status_bar(self):
        cursor = self.text_editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        self.line_col_label.setText(f"Ln {line}, Col {col}")

        char_count = len(self.text_editor.toPlainText())
        self.char_count_label.setText(f"Length: {char_count}")

        font_size = self.text_editor.font().pointSize()
        zoom_percent = round((font_size / self.text_editor.DEFAULT_FONT_SIZE) * 100)
        self.zoom_label.setText(f"Zoom: {zoom_percent}%")

        self.crypto_status_label.setText("Encrypted (AES-256)" if self.is_encrypted else "Plaintext")

    # ---------------- Zoom ----------------
    def zoom_editor(self, factor):
        font = self.text_editor.font()
        current_size = font.pointSize()
        new_size = max(8, min(48, current_size + factor))
        font.setPointSize(new_size)
        self.text_editor.setFont(font)
        self.update_status_bar()

    def zoom_in(self):
        self.zoom_editor(1)

    def zoom_out(self):
        self.zoom_editor(-1)

    def reset_zoom(self):
        font = self.text_editor.font()
        font.setPointSize(self.text_editor.DEFAULT_FONT_SIZE)
        self.text_editor.setFont(font)
        self.update_status_bar()

    # ---------------- Menu ----------------
    def init_menu(self):
        menu = self.menuBar()

        # --- File ---
        file_menu = menu.addMenu("&File")

        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # --- Edit ---
        edit_menu = menu.addMenu("&Edit")
        edit_menu.addAction(QAction("&Undo", self, shortcut="Ctrl+Z", triggered=self.text_editor.undo))
        edit_menu.addAction(QAction("&Redo", self, shortcut="Ctrl+Y", triggered=self.text_editor.redo))
        edit_menu.addSeparator()
        edit_menu.addAction(QAction("Cu&t", self, shortcut="Ctrl+X", triggered=self.text_editor.cut))
        edit_menu.addAction(QAction("&Copy", self, shortcut="Ctrl+C", triggered=self.text_editor.copy))
        edit_menu.addAction(QAction("&Paste", self, shortcut="Ctrl+V", triggered=self.text_editor.paste))

        # --- View ---
        view_menu = menu.addMenu("&View")
        toggle_status_action = QAction("&Status Bar", self, checkable=True)
        toggle_status_action.setChecked(True)
        toggle_status_action.triggered.connect(lambda checked: self.statusBar.setVisible(checked))
        view_menu.addAction(toggle_status_action)

        zoom_menu = view_menu.addMenu("&Zoom")
        zoom_menu.addAction(QAction("Zoom In", self, shortcut="Ctrl++", triggered=self.zoom_in))
        zoom_menu.addAction(QAction("Zoom Out", self, shortcut="Ctrl+-", triggered=self.zoom_out))
        zoom_menu.addAction(QAction("Reset Zoom (100%)", self, shortcut="Ctrl+0", triggered=self.reset_zoom))

        # --- Help ---
        help_menu = menu.addMenu("&Help")
        help_menu.addAction(QAction("&About", self, triggered=self.show_about_dialog))

    # ---------------- File Operations ----------------
    def new_file(self):
        self.text_editor.clear()
        self.text_editor.document().setModified(False)
        self.current_file = None
        self.is_encrypted = False
        self.setWindowTitle("Untitled - Secured Notepad")
        self.update_status_bar()

    def open_file(self):
        from PyQt5.QtWidgets import QLineEdit
        file_filter = "All Files (*);;Text Files (*.txt);;Encrypted Files (*.txt.enc)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", file_filter)
        if not file_path:
            return

        self.current_file = file_path
        self.is_encrypted = file_path.endswith(".txt.enc")

        try:
            if self.is_encrypted:
                if not CRYPTO_AVAILABLE:
                    raise RuntimeError("Cryptography library not available.")
                with open(file_path, "rb") as f:
                    content = f.read()
                if len(content) < 16:
                    raise ValueError("Corrupted encrypted file.")
                salt, token = content[:16], content[16:]
                password, ok = QInputDialog.getText(self, "Decrypt File", f"Password for '{os.path.basename(file_path)}':", QLineEdit.Password)
                if ok and password:
                    plaintext = decrypt_data(token, password, salt)
                    self.text_editor.setPlainText(plaintext)
                else:
                    self.current_file = None
                    self.is_encrypted = False
                    return
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.text_editor.setPlainText(f.read())

            self.setWindowTitle(f"{os.path.basename(file_path)} - Secured Notepad")
            self.text_editor.document().setModified(False)
            self.update_status_bar()

        except Exception as e:
            self.current_file = None
            self.is_encrypted = False
            self.text_editor.clear()
            QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    def save_file(self):
        if self.current_file:
            if self.is_encrypted:
                return self._save_encrypted_flow(self.current_file)
            else:
                return self._save_plaintext_flow(self.current_file)
        else:
            return self.save_file_as()

    def save_file_as(self):
        dialog = SaveModeDialog(self, crypto_available=CRYPTO_AVAILABLE)
        if dialog.exec_() != dialog.Accepted:
            return False

        save_mode = dialog.save_mode
        password = dialog.password

        if save_mode == "plaintext":
            default_path = "untitled.txt"
            if self.current_file and self.current_file.endswith(".txt.enc"):
                default_path = self.current_file.replace(".txt.enc", "")
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Plaintext File As", default_path, "Text Files (*.txt);;All Files (*)")
            if file_path:
                self.current_file = file_path
                return self._save_plaintext_flow(file_path)
        elif save_mode == "encrypted":
            if not password:
                QMessageBox.critical(self, "Error", "Encryption password cannot be empty.")
                return False
            default_name = "untitled.txt.enc"
            if self.current_file:
                default_name = os.path.basename(self.current_file).replace(".txt", "").replace(".enc", "") + ".txt.enc"
            default_path = os.path.join(os.path.dirname(self.current_file) if self.current_file else os.getcwd(), default_name)
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Encrypted File As", default_path, "Encrypted Files (*.txt.enc)")
            if file_path:
                if not file_path.endswith(".txt.enc"):
                    file_path += ".txt.enc"
                self.current_file = file_path
                return self._save_encrypted_flow(file_path, password=password)

        return False

    # ---------------- Internal Save Flows ----------------
    def _save_plaintext_flow(self, file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.text_editor.toPlainText())
            self.is_encrypted = False
            self.text_editor.document().setModified(False)
            self.setWindowTitle(f"{os.path.basename(file_path)} - Secured Notepad")
            self.update_status_bar()
            self.statusBar.showMessage(f"Saved (Plaintext): {os.path.basename(file_path)}", 5000)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save plaintext file: {e}")
            return False

    def _save_encrypted_flow(self, file_path, password=None):
        from PyQt5.QtWidgets import QLineEdit
        if not CRYPTO_AVAILABLE:
            QMessageBox.critical(self, "Error", "Cryptography library not available. Cannot save encrypted.")
            return False

        if password is None:
            password, ok = QInputDialog.getText(
                self, "Set Password", "Enter password for encryption:", QLineEdit.Password
            )
            if not ok or not password:
                self.statusBar.showMessage("Encryption cancelled.", 5000)
                return False

        try:
            token, salt = encrypt_data(self.text_editor.toPlainText(), password)
            with open(file_path, "wb") as f:
                f.write(salt + token)
            self.is_encrypted = True
            self.text_editor.document().setModified(False)
            self.setWindowTitle(f"{os.path.basename(file_path)} - Secured Notepad")
            self.update_status_bar()
            self.statusBar.showMessage(f"Saved (Encrypted): {os.path.basename(file_path)}", 5000)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Encryption Error", f"Could not encrypt and save file: {e}")
            return False

        # ---------------- About Dialog ----------------

    def show_about_dialog(self):
        crypto_status = "Available" if CRYPTO_AVAILABLE else "Disabled (Install 'cryptography')"
        QMessageBox.information(
            self,
            "About Secured Notepad",
            f"Secured Notepad\n\nBuilt with Python & PyQt5.\n\n"
            f"Features:\n- Line numbering\n- Dark theme\n- Professional menus\n"
            f"- Status bar with line/column, char count, zoom, encryption status\n"
            f"- AES-256 Encryption support\n\nEncryption library: {crypto_status}"
        )

        # ---------------- Close Event ----------------

    def closeEvent(self, event):
        if self.text_editor.document().isModified():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "Do you want to save your changes before exiting?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                if self.save_file():
                    event.accept()
                else:
                    event.ignore()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

        # ---------------- Main ----------------

    if __name__ == "__main__":
        import sys
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QApplication

        if hasattr(Qt, "AA_EnableHighDpiScaling"):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, "AA_UseHighDpiPixmaps"):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        app = QApplication(sys.argv)
        window = EnhancedNotepad()
        window.show()
        sys.exit(app.exec_())
