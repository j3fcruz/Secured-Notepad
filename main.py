"""
main.py
-------
Entry point for Enhanced Notepad.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QFile, QTextStream
from notepad import EnhancedNotepad
import resources_rc  # compiled from your .qrc

if __name__ == "__main__":

    # High DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Load theme from resource
    THEME_FILE = QFile(":/assets/themes/dark_theme.qss")
    if THEME_FILE.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(THEME_FILE)
        app.setStyleSheet(stream.readAll())

    # Create main window
    window = EnhancedNotepad()

    # Set icon from resource
    window.setWindowIcon(QIcon(":/assets/icons/icon.png"))

    window.show()
    sys.exit(app.exec_())
