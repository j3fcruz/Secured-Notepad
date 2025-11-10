"""
 modules/tab_manager.py
Manages multiple text editor tabs with metadata tracking.
"""

from PyQt5.QtWidgets import QTabWidget, QMessageBox
from PyQt5.QtCore import QObject
from utils.editor import EnhancedTextEditor

class TabManager(QObject):
    """Handles multi-tab operations and metadata tracking."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # --- Do NOT connect to status_manager here ---
        # self.tabs.currentChanged.connect(self.parent.status_manager.update_status_bar)

        # Metadata per tab: {index: {"path": ..., "encrypted": ..., "password": ...}}
        self.tab_files = {}

        # Default font size for zoom
        self.default_font_size = 12

    # --- Allow external connection to status_manager later ---
    def connect_status_manager(self, status_manager):
        self.tabs.currentChanged.connect(status_manager.update_status_bar)

    def current_editor(self):
        editor = self.tabs.currentWidget()
        if isinstance(editor, EnhancedTextEditor):
            return editor
        return None

    def current_tab_index(self):
        return self.tabs.currentIndex()

    def current_tab_data(self):
        return self.tab_files.get(self.current_tab_index(), {})

    def new_tab(self, path=None, content="", encrypted=False, password=None):
        editor = EnhancedTextEditor()
        editor.setPlainText(content)
        editor.document().setModified(False)

        # Connect editor signals to status_manager if available
        if hasattr(self.parent, "status_manager"):
            editor.cursorPositionChanged.connect(self.parent.status_manager.update_status_bar)
            editor.textChanged.connect(self.parent.status_manager.update_status_bar)

        index = self.tabs.addTab(editor, path if path else "Untitled")
        self.tabs.setCurrentIndex(index)
        self.tab_files[index] = {"path": path, "encrypted": encrypted, "password": password}

        # Set default font size if not already
        if not self.default_font_size:
            self.default_font_size = editor.font().pointSize()

    def close_tab(self, index):
        editor = self.tabs.widget(index)
        if editor.document().isModified():
            reply = QMessageBox.question(
                self.tabs, "Unsaved Changes",
                f"Tab '{self.tabs.tabText(index)}' has unsaved changes. Save?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.tabs.setCurrentIndex(index)
                if hasattr(self.parent, "file_handler"):
                    if not self.parent.file_handler.save_file():
                        return
            elif reply == QMessageBox.Cancel:
                return
        self.tabs.removeTab(index)
        self.tab_files.pop(index, None)
