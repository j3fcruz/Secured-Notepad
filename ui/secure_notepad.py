"""
Secure Notepad Pro - Combined Working Version
(Zoom + Save both functional)
"""

import os
import webbrowser
import subprocess
import logging
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QStatusBar, QAction, QFileDialog,
    QMessageBox, QInputDialog, QTabWidget
)
from PyQt5.QtCore import Qt, QTimer

from utils.editor import EnhancedTextEditor
from utils.encryption import encrypt_data, decrypt_data, CRYPTO_AVAILABLE
from utils.icon_manager import load_icon

from dialogs.save_dialog import SaveModeDialog
from dialogs.about_dialog import AboutDialog
from dialogs.donate_dialog import DonateDialog
from dialogs.help_dialog import HelpDialog
from dialogs.terms_conditions_dialog import TermsConditionsDialog
from dialogs.license_dialog import LicenseDialog


logging.basicConfig(level=logging.INFO)


class EnhancedNotepad(QMainWindow):
    AUTOSAVE_INTERVAL_MS = 60000  # 60 seconds

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Untitled - Secure Notepad Pro")
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(load_icon("notepad.png"))

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_status_bar)
        self.setCentralWidget(self.tabs)

        self.tab_files = {}
        self.default_font_size = 12

        self.init_status_bar()
        self.init_menu()

        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave_all_tabs)
        self.autosave_timer.start(self.AUTOSAVE_INTERVAL_MS)

        self.new_tab()

    # ---------------- Tab Helpers ----------------
    def current_editor(self):
        editor = self.tabs.currentWidget()
        return editor if isinstance(editor, EnhancedTextEditor) else None

    def current_tab_index(self):
        return self.tabs.currentIndex()

    def current_tab_data(self):
        return self.tab_files.get(self.current_tab_index(), {})

    # ---------------- Status Bar ----------------
    def init_status_bar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.line_col_label = QLabel("Ln 1, Col 1")
        self.char_count_label = QLabel("Length: 0")
        self.encoding_label = QLabel("UTF-8")
        self.crypto_status_label = QLabel("Plaintext")
        self.crlf_label = QLabel("CRLF")
        self.zoom_label = QLabel("Zoom: 100%")

        for w in [
            self.line_col_label, "|",
            self.char_count_label, "|",
            self.encoding_label, "|",
            self.crypto_status_label, "|",
            self.crlf_label, "|",
            self.zoom_label
        ]:
            self.statusBar.addPermanentWidget(QLabel(w) if isinstance(w, str) else w)
        self.update_status_bar()

    def update_status_bar(self):
        if getattr(self, "_updating_status", False):
            return
        self._updating_status = True
        try:
            editor = self.current_editor()
            if not editor:
                return
            cursor = editor.textCursor()
            self.line_col_label.setText(f"Ln {cursor.blockNumber() + 1}, Col {cursor.columnNumber()}")
            self.char_count_label.setText(f"Length: {len(editor.toPlainText())}")
            font_size = editor.font().pointSize()
            zoom_percent = round((font_size / self.default_font_size) * 100)
            self.zoom_label.setText(f"Zoom: {zoom_percent}%")
            tab_data = self.current_tab_data()
            self.crypto_status_label.setText("Encrypted (AES-256)" if tab_data.get("encrypted") else "Plaintext")
        finally:
            self._updating_status = False

    # ---------------- Tab Management ----------------
    def new_tab(self, path=None, content="", encrypted=False, password=None):
        editor = EnhancedTextEditor()
        editor.setPlainText(content)
        editor.document().setModified(False)
        editor.cursorPositionChanged.connect(self.update_status_bar)
        editor.textChanged.connect(self.update_status_bar)
        # ✅ fix: enable mouse wheel zoom
        editor.set_wheel_zoom_callback(self.zoom_editor)

        index = self.tabs.addTab(editor, os.path.basename(path) if path else "Untitled")
        self.tabs.setCurrentIndex(index)
        self.tab_files[index] = {"path": path, "encrypted": encrypted, "password": password}
        if not self.default_font_size:
            self.default_font_size = editor.font().pointSize()

    def close_tab(self, index):
        editor = self.tabs.widget(index)
        if editor.document().isModified():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                f"Tab '{self.tabs.tabText(index)}' has unsaved changes. Save?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.tabs.setCurrentIndex(index)
                if not self.save_file():
                    return
            elif reply == QMessageBox.Cancel:
                return
        self.tabs.removeTab(index)
        self.tab_files.pop(index, None)

    # ---------------- Zoom ----------------
    def zoom_editor(self, delta):
        editor = self.current_editor()
        if not editor:
            return
        font = editor.font()
        new_size = max(8, min(48, font.pointSize() + delta))
        font.setPointSize(new_size)
        editor.setFont(font)
        self.update_status_bar()

    def zoom_in(self): self.zoom_editor(1)
    def zoom_out(self): self.zoom_editor(-1)
    def reset_zoom(self):
        editor = self.current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(self.default_font_size)
            editor.setFont(font)
            self.update_status_bar()

    # ---------------- Menu Bar ----------------
    def init_menu(self):
        menu = self.menuBar()

        # --- File Menu ---
        file_menu = menu.addMenu("&File")
        file_menu.addAction(QAction("&New Tab", self, shortcut="Ctrl+T", triggered=self.new_tab))
        file_menu.addAction(QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open_file))
        file_menu.addAction(QAction("&Save", self, shortcut="Ctrl+S", triggered=self.save_file))
        file_menu.addAction(QAction("Save &As...", self, shortcut="Ctrl+Shift+S", triggered=self.save_file_as))
        file_menu.addSeparator()
        file_menu.addAction(QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close))

        # --- Edit Menu ---
        edit_menu = menu.addMenu("&Edit")
        edit_menu.addAction(QAction("&Undo", self, shortcut="Ctrl+Z", triggered=lambda: self.current_editor().undo()))
        edit_menu.addAction(QAction("&Redo", self, shortcut="Ctrl+Y", triggered=lambda: self.current_editor().redo()))
        edit_menu.addSeparator()
        edit_menu.addAction(QAction("Cu&t", self, shortcut="Ctrl+X", triggered=lambda: self.current_editor().cut()))
        edit_menu.addAction(QAction("&Copy", self, shortcut="Ctrl+C", triggered=lambda: self.current_editor().copy()))
        edit_menu.addAction(QAction("&Paste", self, shortcut="Ctrl+V", triggered=lambda: self.current_editor().paste()))

        # --- View Menu ---
        view_menu = menu.addMenu("&View")
        toggle_status = QAction("&Status Bar", self, checkable=True, checked=True)
        toggle_status.triggered.connect(lambda v: self.statusBar.setVisible(v))
        view_menu.addAction(toggle_status)

        zoom_menu = view_menu.addMenu("&Zoom")
        zoom_menu.addAction(QAction("Zoom In", self, shortcut="Ctrl++", triggered=self.zoom_in))
        zoom_menu.addAction(QAction("Zoom Out", self, shortcut="Ctrl+-", triggered=self.zoom_out))
        zoom_menu.addAction(QAction("Reset Zoom (100%)", self, shortcut="Ctrl+0", triggered=self.reset_zoom))

        # --- Help Menu ---
        help_menu = menu.addMenu("&Help")

        # --- Documentation Section ---
        doc_menu = help_menu.addMenu("📖 Documentation")
        doc_menu.addAction(QAction("Help File (PDF)", self, triggered=self.load_pdf_from_resource))
        doc_menu.addAction(QAction("Help Topics", self, triggered=self.show_help_dialog))

        # --- Support Section ---
        support_menu = help_menu.addMenu("💬 Support")
        support_menu.addAction(QAction("Submit Feedback", self, triggered=self.open_feedback_page))
        support_menu.addAction(QAction("Homepage", self, triggered=self.open_homepage))
        support_menu.addAction(QAction("💝 Donate", self, triggered=self.show_donate_dialog))

        # --- Legal & About Section ---
        legal_menu = help_menu.addMenu("ℹ️ About & Legal")
        legal_menu.addAction(QAction("About", self, triggered=self.show_about_dialog))
        legal_menu.addAction(QAction("Terms & Conditions", self, triggered=self.show_terms_conditions_dialog))
        legal_menu.addAction(QAction("License Agreement", self, triggered=self.show_license_dialog))

    # ---------------- File Handling ----------------
    def open_file(self):
        from PyQt5.QtWidgets import QLineEdit

        file_filter = "All Files (*);;Text Files (*.txt);;Encrypted Files (*.txt.enc)"
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", file_filter)
        if not path:
            return

        try:
            if path.endswith(".enc"):
                if not CRYPTO_AVAILABLE:
                    raise RuntimeError("Cryptography module not available")

                with open(path, "rb") as f:
                    data = f.read()

                salt, token = data[:16], data[16:]

                password, ok = QInputDialog.getText(self, "Decrypt File", "Enter password:", QLineEdit.Password)
                if not ok or not password:
                    return

                try:
                    plaintext = decrypt_data(token, password, salt)
                    self.statusBar.showMessage("File open successfully!", 4000)
                except Exception:
                    # Password incorrect or decryption failed
                    QMessageBox.warning(self, "Decryption Error", "Incorrect password or corrupted file!")
                    self.statusBar.showMessage("Failed to open encrypted file: incorrect password", 4000)
                    return

                self.new_tab(path, plaintext, True, password)
            else:
                with open(path, "r", encoding="utf-8") as f:
                    self.new_tab(path, f.read(), False)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_file(self):
        index = self.current_tab_index()
        tab_data = self.current_tab_data()
        path = tab_data.get("path")
        if path:
            return self._save_plaintext_flow(path, index)
        return self.save_file_as()

    def save_file_as(self):
        dialog = SaveModeDialog(self, crypto_available=CRYPTO_AVAILABLE)
        if dialog.exec_() != dialog.Accepted:
            return False
        save_mode = dialog.save_mode
        password = dialog.password
        index = self.current_tab_index()

        if save_mode == "plaintext":
            path, _ = QFileDialog.getSaveFileName(self, "Save File As", "untitled.txt", "Text Files (*.txt)")
            if path:
                return self._save_plaintext_flow(path, index)
        elif save_mode == "encrypted":
            path, _ = QFileDialog.getSaveFileName(self, "Save Encrypted File As", "untitled.txt.enc", "Encrypted Files (*.txt.enc)")
            if path:
                return self._save_encrypted_flow(path, password, index)
        return False

    def _save_plaintext_flow(self, path, index):
        try:
            editor = self.tabs.widget(index)
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
            self.tab_files[index] = {"path": path, "encrypted": False, "password": None}
            self.tabs.setTabText(index, os.path.basename(path))
            editor.document().setModified(False)
            self.statusBar.showMessage(f"Saved: {os.path.basename(path)}", 5000)
            self.update_status_bar()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Save failed:\n{e}")
            return False

    def _save_encrypted_flow(self, path, password, index):
        try:
            editor = self.tabs.widget(index)
            token, salt = encrypt_data(editor.toPlainText(), password)
            with open(path, "wb") as f:
                f.write(salt + token)
            self.tab_files[index] = {"path": path, "encrypted": True, "password": password}
            self.tabs.setTabText(index, os.path.basename(path))
            editor.document().setModified(False)
            self.statusBar.showMessage(f"Encrypted Save: {os.path.basename(path)}", 5000)
            self.update_status_bar()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Encryption failed:\n{e}")
            return False

    # ---------------- Autosave ----------------
    def autosave_all_tabs(self):
        for i in range(self.tabs.count()):
            ed = self.tabs.widget(i)
            if not ed or not ed.document().isModified():
                continue
            d = self.tab_files.get(i, {})
            path = d.get("path")
            if path:
                self._save_plaintext_flow(path, i)

    # ---------------- Help & Dialogs ----------------
    def open_help_file(self):
        """Open help PDF file"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "assets", "docs", "help.pdf"),
            os.path.join(os.getcwd(), "assets", "docs", "help.pdf"),
            os.path.join(os.getcwd(), "help.pdf"),
        ]
        help_file = next((p for p in possible_paths if os.path.exists(p)), None)
        if help_file:
            if os.name == 'nt':
                os.startfile(help_file)
            else:
                try:
                    subprocess.Popen(['open', help_file])
                except:
                    try:
                        subprocess.Popen(['xdg-open', help_file])
                    except:
                        pass
        else:
            QMessageBox.warning(self, "Help Not Found", "help.pdf not found in the expected locations")

    def load_pdf_from_resource_embed(self):
        """Safely load embedded Help PDF from resources (qrc) or fallback to external viewer."""
        try:
            if not PDF_SUPPORT:
                # PDF modules not available → fallback to external help file
                self.open_help_file()
                return

            # Try loading embedded PDF from resources
            file = QFile(":/assets/docs/help.pdf")
            if not file.exists():
                self.statusBar.showMessage("Embedded help not found, using external viewer...", 4000)
                self.open_help_file()
                return

            if not file.open(QIODevice.ReadOnly):
                QMessageBox.warning(self, "Error", "Unable to open embedded help file resource.")
                return

            data = file.readAll()
            file.close()

            # Create and validate QPdfDocument
            self.pdf_doc = QPdfDocument(self)
            load_status = self.pdf_doc.loadFromData(data)
            if load_status != QPdfDocument.Status.Ready:
                QMessageBox.warning(self, "Error", "Invalid or unreadable PDF document.")
                return

            # Create PDF viewer window
            pdf_view = QPdfView()
            pdf_view.setDocument(self.pdf_doc)
            pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)

            pdf_window = QMainWindow(self)
            pdf_window.setWindowTitle("📘 Secure Notepad Pro – Help")
            pdf_window.setCentralWidget(pdf_view)
            pdf_window.resize(900, 700)
            pdf_window.show()

            # Keep reference alive
            self._pdf_window = pdf_window
            self.statusBar.showMessage("Help PDF loaded successfully", 3000)

        except Exception as e:
            # Safety fallback: never crash, show error and open external help
            QMessageBox.warning(
                self,
                "PDF Viewer Error",
                f"Failed to load embedded help:\n{str(e)}\n\nOpening external help file instead."
            )
            self.open_help_file()

    def load_pdf_from_resource(self):
        """Load Help PDF directly from assets/docs folder."""
        try:
            # Absolute path to your help PDF
            local_path = os.path.join(os.path.dirname(__file__), "assets", "docs", "help.pdf")
            local_path = os.path.abspath(local_path)

            if not os.path.exists(local_path):
                self.statusBar.showMessage("Help PDF not found, opening external help...", 4000)
                self.open_help_file()
                return

            # Load PDF document
            self.pdf_doc = QPdfDocument(self)
            load_status = self.pdf_doc.load(local_path)
            if load_status != QPdfDocument.Status.Ready:
                QMessageBox.warning(self, "Error", "Invalid or unreadable PDF document.")
                return

            # Show PDF in a window
            pdf_view = QPdfView()
            pdf_view.setDocument(self.pdf_doc)
            pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)

            pdf_window = QMainWindow(self)
            pdf_window.setWindowTitle("📘 Secure Notepad Pro – Help")
            pdf_window.setCentralWidget(pdf_view)
            pdf_window.resize(900, 700)
            pdf_window.show()

            # Keep reference alive
            self._pdf_window = pdf_window
            self.statusBar.showMessage("Help PDF loaded successfully", 3000)

        except Exception as e:
            QMessageBox.warning(
                self,
                "PDF Viewer Error",
                f"Failed to load help PDF:\n{str(e)}\n\nOpening external help file instead."
            )
            self.open_help_file()

    def open_feedback_page(self):
        webbrowser.open("https://www.patronhubdevs.online/contact")
        self.statusBar.showMessage("Opening feedback page...", 3000)

    def open_homepage(self):
        webbrowser.open("https://www.patronhubdevs.online")
        self.statusBar.showMessage("Opening homepage...", 3000)

    def show_about_dialog(self): AboutDialog(self).exec_()
    def show_donate_dialog(self): DonateDialog(self).exec_()
    def show_help_dialog(self): HelpDialog(self).exec_()
    def show_terms_conditions_dialog(self): TermsConditionsDialog(self).exec_()
    def show_license_dialog(self): LicenseDialog(self).exec_()

    # ---------------- Close Event ----------------
    def closeEvent(self, event):
        unsaved_tabs = [i for i in range(self.tabs.count()) if self.tabs.widget(i).document().isModified()]
        for index in unsaved_tabs:
            self.tabs.setCurrentIndex(index)
            editor = self.tabs.widget(index)
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                f"Tab '{self.tabs.tabText(index)}' has unsaved changes. Save?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                if not self.save_file():
                    event.ignore()
                    return
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        event.accept()


if __name__ == "__main__":
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = EnhancedNotepad()
    window.show()
    sys.exit(app.exec_())