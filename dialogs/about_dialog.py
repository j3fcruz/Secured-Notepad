"""
about_dialog.py
================

About Dialog for Secure Notepad Pro v2.0.0

Displays version, author info, website, license, and support links.

Author      : Marco Polo (PatronHub)
Website     : https://patronhubdevs.online
GitHub      : https://github.com/j3fcruz
Ko-fi       : https://ko-fi.com/marcopolo55681
Created     : 2025-11-10
License     : MIT License
"""

import webbrowser
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from utils.path_utils import PathResolver
from config.app_config import APP_NAME, APP_VERSION, APP_DEVELOPER, AUTHOR
from utils.icon_manager import load_icon   # ✅ Correct import


class AboutDialog(QDialog):
    """About dialog showing application information."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")
        self.setFixedSize(520, 420)
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # --- Header section ---
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        # App icon
        icon_label = QLabel()
        icon_label.setFixedSize(72, 72)

        app_icon = load_icon("app_icon.png")  # ✅ Use function directly
        if not app_icon.isNull():
            icon_label.setPixmap(app_icon.pixmap(64, 64))
        else:
            icon_label.setStyleSheet("""
                QLabel {
                    background-color: #0078D4;
                    border-radius: 36px;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                }
            """)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setText("SN")  # Secure Notepad initials

        header_layout.addWidget(icon_label)

        # App title and version
        title_layout = QVBoxLayout()
        title_label = QLabel(APP_NAME)
        title_font = QFont("Segoe UI", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)

        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        title_layout.addWidget(version_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        layout.addWidget(header_frame)

        # --- Separator ---
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # --- Description section ---
        description = QTextEdit()
        description.setReadOnly(True)
        description.setMaximumHeight(180)
        description.setHtml("""
        <h3>Secure Notepad Pro</h3>
        <p><b>Secure Notepad Pro</b> is an enterprise-grade, privacy-focused text editor 
        designed for professionals who need encrypted, organized, and visually elegant note-taking.</p>
        <ul>
            <li><b>Encryption</b> — Built-in AES-GCM encryption for sensitive notes.</li>
            <li><b>Auto Theme</b> — Adapts to system dark/light mode automatically.</li>
            <li><b>High-DPI Support</b> — Scales beautifully on modern 4K displays.</li>
            <li><b>Modular Design</b> — Cleanly separated UI, themes, and logic for scalability.</li>
        </ul>
        <p>Secure Notepad Pro combines strong encryption with a minimalist design, 
        giving you both security and elegance in one lightweight app.</p>
        """)
        layout.addWidget(description)

        # --- Footer / Credits ---
        credits_label = QLabel()
        credits_label.setWordWrap(True)
        credits_label.setText(
            f"Developed by {AUTHOR} – {APP_DEVELOPER}\n\n"
            f"© 2025 {APP_NAME}. All rights reserved.\n"
            "Powered by PyQt5, Python 3, and modern UI/UX practices."
        )
        credits_label.setStyleSheet("color: #aaaaaa; font-size: 11px;")
        layout.addWidget(credits_label)


        # --- Support Buttons Section ---
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Website Button
        website_btn = QPushButton("PatronHubDevs")
        website_btn.clicked.connect(lambda: webbrowser.open("https://patronhubdevs.online"))
        buttons_layout.addWidget(website_btn)

        # GitHub Button
        github_btn = QPushButton("GitHub")
        github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/j3fcruz"))
        buttons_layout.addWidget(github_btn)

        # Ko-fi Button
        kofi_btn = QPushButton("My Ko-fi")
        kofi_btn.clicked.connect(lambda: webbrowser.open("https://ko-fi.com/marcopolo55681"))
        buttons_layout.addWidget(kofi_btn)

        # OK Button
        ok_btn = QPushButton("OK")
        ok_btn.setFixedWidth(80)
        ok_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_btn)

        layout.addLayout(buttons_layout)

        # --- Final Polish ---
        self.setStyleSheet("""
            /* Main Dialog */
            QDialog {
                background-color: #0f0f1e;
                color: #e0e0e6;
            }

            /* Text Edit */
            QTextEdit {
                background-color: #1a1a2e;
                color: #c0c0d0;
                border: 1px solid #3d3d5c;
                border-radius: 6px;
                padding: 8px;
                font-family: "Segoe UI", "Consolas", monospace;
                font-size: 12px;
            }
            QTextEdit:focus {
                border: 2px solid #6366f1;
                background-color: #16213e;
            }

            /* Line Edit */
            QLineEdit {
                background-color: #1a1a2e;
                color: #c0c0d0;
                border: 1px solid #3d3d5c;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #6366f1;
                background-color: #16213e;
            }

            /* Push Button */
            QPushButton {
                background-color: #0078D4;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }

            /* Labels */
            QLabel {
                color: #b0b0c0;
                font-size: 12px;
            }

            /* Combo Box */
            QComboBox {
                background-color: #1a1a2e;
                color: #c0c0d0;
                border: 1px solid #3d3d5c;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QComboBox:focus {
                border: 2px solid #6366f1;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #16213e;
            }
            QComboBox::down-arrow {
                image: url(noimg);
                width: 12px;
                height: 12px;
            }

            /* Combo Box Item List */
            QComboBox QAbstractItemView {
                background-color: #16213e;
                color: #c0c0d0;
                border: 1px solid #3d3d5c;
                selection-background-color: #6366f1;
                selection-color: #ffffff;
                font-size: 12px;
            }

            /* Spin Box */
            QSpinBox, QDoubleSpinBox {
                background-color: #1a1a2e;
                color: #c0c0d0;
                border: 1px solid #3d3d5c;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #6366f1;
            }

            /* Checkbox */
            QCheckBox {
                color: #b0b0c0;
                spacing: 8px;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #3d3d5c;
                background-color: #1a1a2e;
            }
            QCheckBox::indicator:checked {
                background-color: #6366f1;
                border: 1px solid #6366f1;
            }

            /* Radio Button */
            QRadioButton {
                color: #b0b0c0;
                spacing: 8px;
                font-size: 12px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 1px solid #3d3d5c;
                background-color: #1a1a2e;
            }
            QRadioButton::indicator:checked {
                background-color: #6366f1;
                border: 1px solid #6366f1;
            }

            /* Group Box */
            QGroupBox {
                color: #b0b0c0;
                border: 1px solid #3d3d5c;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }

            /* Scroll Bar */
            QScrollBar:vertical {
                background-color: #16213e;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #3d3d5c;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6366f1;
            }
            QScrollBar:horizontal {
                background-color: #16213e;
                height: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background-color: #3d3d5c;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #6366f1;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                border: none;
                background: none;
            }

            /* Menu Bar */
            QMenuBar {
                background-color: #0f0f1e;
                color: #b0b0c0;
                border-bottom: 1px solid #3d3d5c;
                font-size: 12px;
            }
            QMenuBar::item:selected {
                background-color: #16213e;
            }

            /* Menu */
            QMenu {
                background-color: #16213e;
                color: #b0b0c0;
                border: 1px solid #3d3d5c;
                border-radius: 6px;
                font-size: 12px;
            }
            QMenu::item:selected {
                background-color: #6366f1;
                color: #ffffff;
            }

            /* Table Widget */
            QTableWidget {
                background-color: #1a1a2e;
                color: #c0c0d0;
                border: 1px solid #3d3d5c;
                gridline-color: #3d3d5c;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 4px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #6366f1;
                color: #ffffff;
            }

            /* Table Header */
            QHeaderView::section {
                background-color: #16213e;
                color: #b0b0c0;
                padding: 8px;
                border: none;
                border-right: 1px solid #3d3d5c;
                border-bottom: 1px solid #3d3d5c;
                font-weight: bold;
                font-size: 12px;
            }

            /* Tree Widget */
            QTreeWidget {
                background-color: #1a1a2e;
                color: #c0c0d0;
                border: 1px solid #3d3d5c;
                gridline-color: #3d3d5c;
                font-size: 12px;
            }
            QTreeWidget::item:selected {
                background-color: #6366f1;
                color: #ffffff;
            }

            /* Tab Widget */
            QTabWidget::pane {
                border: 1px solid #3d3d5c;
                background-color: #0f0f1e;
            }
            QTabBar::tab {
                background-color: #16213e;
                color: #b0b0c0;
                padding: 6px 20px;
                border: 1px solid #3d3d5c;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #6366f1;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #3d3d5c;
            }

            /* Slider */
            QSlider::groove:horizontal {
                background-color: #3d3d5c;
                height: 8px;
                border-radius: 4px;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background-color: #6366f1;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background-color: #818cf8;
            }

            /* Progress Bar */
            QProgressBar {
                background-color: #16213e;
                color: #b0b0c0;
                border: 1px solid #3d3d5c;
                border-radius: 6px;
                text-align: center;
                height: 24px;
                font-size: 12px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #6366f1;
                border-radius: 4px;
            }

            /* Plain Text Edit */
            QPlainTextEdit {
                background-color: #1a1a2e;
                color: #c0c0d0;
                border: 1px solid #3d3d5c;
                border-radius: 6px;
                padding: 8px;
                font-family: "Segoe UI", "Consolas", monospace;
                font-size: 12px;
            }
            QPlainTextEdit:focus {
                border: 2px solid #6366f1;
                background-color: #16213e;
            }

            /* Tooltip */
            QToolTip {
                background-color: #16213e;
                color: #c0c0d0;
                border: 2px solid #6366f1;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 11px;
                font-weight: 500;
            }

            /* Status Bar */
            QStatusBar {
                background-color: #0f0f1e;
                color: #b0b0c0;
                border-top: 1px solid #3d3d5c;
                font-size: 11px;
            }

            /* Tool Bar */
            QToolBar {
                background-color: #0f0f1e;
                border: none;
                spacing: 6px;
            }
            QToolButton {
                background-color: transparent;
                color: #b0b0c0;
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QToolButton:hover {
                background-color: #16213e;
                border: 1px solid #3d3d5c;
            }
            QToolButton:pressed {
                background-color: #6366f1;
                color: #ffffff;
            }
        """)
