"""
main.py
=======

Entry point for **Secure Notepad Pro v2.0.0** – a professional, encrypted note-taking application.

This script initializes the QApplication, loads themes/icons safely, and starts the main window.
It is production-ready with logging, error handling, and PyInstaller compatibility.

Author      : Marco Polo (PatronHub)
Website     : https://patronhubdevs.online
GitHub      : https://github.com/j3fcruz
Ko-fi       : https://ko-fi.com/marcopolo55681
Created     : 2025-11-10
License     : MIT License
Dependencies: PyQt5 >= 5.15.7, cryptography >= 41.0.0 (optional)
"""

import sys
import os
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox

# -----------------------------------------------------
# Helper: Get Absolute Resource Path
# -----------------------------------------------------
def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and PyInstaller.
    """
    try:
        # PyInstaller stores files in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -----------------------------------------------------
# Add current directory to sys.path to safely import packages
# -----------------------------------------------------
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# -----------------------------------------------------
# Import Main Window
# -----------------------------------------------------
try:
    from ui.secure_notepad import EnhancedNotepad
except ImportError as e:
    logging.exception("Failed to import EnhancedNotepad from ui.secure_notepad")
    QMessageBox.critical(None, "Import Error", f"Cannot import main window:\n{e}")
    sys.exit(1)

# -----------------------------------------------------
# Optional Safe Imports
# -----------------------------------------------------
try:
    from utils.theme_manager import load_theme
except ImportError:
    load_theme = None
    logging.warning("Theme manager not found. Skipping theme loading.")

try:
    from utils.icon_manager import load_icon
except ImportError:
    load_icon = None
    logging.warning("Icon manager not found. Skipping icon loading.")

# -----------------------------------------------------
# Configure Logging
# -----------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# -----------------------------------------------------
# Main Entry Point
# -----------------------------------------------------
def main():
    """Start Secure Notepad Pro (production)."""
    try:
        # Enable High DPI Scaling
        if hasattr(Qt, "AA_EnableHighDpiScaling"):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, "AA_UseHighDpiPixmaps"):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        # Create QApplication
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(True)

        # Load Theme (Safe)
        if load_theme:
            try:
                load_theme(app)
                logging.info("Theme loaded successfully.")
            except Exception as e:
                logging.exception("Failed to load theme. Continuing without theme.")

        # Initialize Main Window
        try:
            window = EnhancedNotepad()
        except Exception as e:
            logging.exception("Failed to initialize main window.")
            QMessageBox.critical(None, "Startup Error", f"Failed to initialize main window:\n\n{e}")
            sys.exit(1)

        # Load Window Icon (Safe)
        if load_icon:
            try:
                icon = load_icon("icon.png")
                if icon:
                    window.setWindowIcon(icon)
            except Exception as e:
                logging.warning(f"Failed to load icon: {e}")

        # Show Window
        try:
            window.show()
        except Exception as e:
            logging.exception("Failed to show main window.")
            QMessageBox.critical(None, "Runtime Error", f"Failed to show main window:\n\n{e}")
            sys.exit(1)

        logging.info("✅ Secure Notepad Pro started successfully.")
        sys.exit(app.exec_())

    except Exception as e:
        logging.exception("Unhandled exception during startup.")
        QMessageBox.critical(None, "Fatal Error", f"An unexpected error occurred:\n\n{e}")
        sys.exit(1)

# -----------------------------------------------------
# Run Main
# -----------------------------------------------------
if __name__ == "__main__":
    logging.info("🚀 Secure Notepad Pro starting in production mode...")
    main()
