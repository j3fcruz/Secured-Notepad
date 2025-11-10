"""
help_dialog.py
---------------
Help and documentation dialog for Secure Notepad Pro.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QTabWidget, QWidget, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config.app_config import APP_NAME


class HelpDialog(QDialog):
    """Help dialog providing usage guide, shortcuts, and troubleshooting."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - Help")
        self.setMinimumSize(750, 520)
        self.setModal(True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Title
        title_label = QLabel(f"{APP_NAME} - Help & Documentation")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tab widget
        tab_widget = QTabWidget()
        tab_widget.addTab(self.create_overview_tab(), "Overview")
        tab_widget.addTab(self.create_shortcuts_tab(), "Keyboard Shortcuts")
        tab_widget.addTab(self.create_encryption_tab(), "Encryption & Security")
        tab_widget.addTab(self.create_theming_tab(), "Themes & Appearance")
        tab_widget.addTab(self.create_troubleshooting_tab(), "Troubleshooting")
        layout.addWidget(tab_widget)

        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_button = QPushButton("Close")
        close_button.setFixedWidth(90)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

        # Style
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

    # ================================
    #   TAB CONTENTS
    # ================================
    def create_overview_tab(self):
        """Overview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml(f"""
        <h2>Welcome to {APP_NAME}</h2>
        <p><b>{APP_NAME}</b> is a professional encrypted text editor designed for privacy, simplicity, 
        and productivity. It allows you to create, save, and manage notes with built-in AES encryption 
        and automatic theme adaptation.</p>

        <h3>Key Features</h3>
        <ul>
            <li><b>End-to-End Encryption:</b> Protect sensitive notes using secure AES-GCM encryption.</li>
            <li><b>Auto Theme Detection:</b> Automatically switches between light and dark themes.</li>
            <li><b>Instant Save & Open:</b> Encrypted files are seamlessly handled in seconds.</li>
            <li><b>High-DPI Scaling:</b> Clean visuals even on 4K displays.</li>
            <li><b>Cross-Platform:</b> Works on Windows, macOS, and Linux.</li>
        </ul>

        <h3>Quick Start</h3>
        <ol>
            <li>Launch {APP_NAME}.</li>
            <li>Start typing your note or open an existing one.</li>
            <li>Click <b>Encrypt Save</b> to store securely with a password.</li>
            <li>Click <b>Decrypt Open</b> to unlock a saved note.</li>
        </ol>
        """)
        layout.addWidget(text)
        return widget

    def create_shortcuts_tab(self):
        """Keyboard shortcuts tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
        <h2>Keyboard Shortcuts</h2>
        <p>Improve your productivity with these keyboard shortcuts:</p>

        <table border="1" cellspacing="0" cellpadding="6" width="100%">
            <tr><th align="left">Action</th><th align="left">Shortcut</th></tr>
            <tr><td>New File</td><td><b>Ctrl + N</b></td></tr>
            <tr><td>Open File</td><td><b>Ctrl + O</b></td></tr>
            <tr><td>Save File</td><td><b>Ctrl + S</b></td></tr>
            <tr><td>Encrypt Save</td><td><b>Ctrl + E</b></td></tr>
            <tr><td>Decrypt Open</td><td><b>Ctrl + D</b></td></tr>
            <tr><td>Find Text</td><td><b>Ctrl + F</b></td></tr>
            <tr><td>Zoom In</td><td><b>Ctrl + +</b></td></tr>
            <tr><td>Zoom Out</td><td><b>Ctrl + -</b></td></tr>
            <tr><td>Reset Zoom</td><td><b>Ctrl + 0</b></td></tr>
            <tr><td>Toggle Dark/Light Mode</td><td><b>Ctrl + T</b></td></tr>
            <tr><td>Show Help</td><td><b>F1</b></td></tr>
        </table>
        """)
        layout.addWidget(text)
        return widget

    def create_encryption_tab(self):
        """Encryption and security tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
        <h2>Encryption & Security</h2>
        <p>{APP_NAME} uses the <b>AES-GCM (Advanced Encryption Standard – Galois/Counter Mode)</b> 
        algorithm for data protection. AES-GCM provides both confidentiality and integrity verification.</p>

        <h3>How It Works</h3>
        <ol>
            <li>Your text is encrypted using your password as a key.</li>
            <li>The encryption process generates a secure random nonce.</li>
            <li>The encrypted content and nonce are stored safely.</li>
            <li>Decryption requires the exact same password.</li>
        </ol>

        <h3>Best Practices</h3>
        <ul>
            <li>Use a strong password (minimum 8–12 characters).</li>
            <li>Keep encrypted files in a secure folder.</li>
            <li>Do not share passwords over insecure channels.</li>
            <li>Backup encrypted files regularly.</li>
        </ul>

        <h3>Security Notice</h3>
        <p>If you forget your password, the encrypted file <b>cannot</b> be recovered. 
        This is by design — even the developers of Secure Notepad Pro cannot decrypt your notes without the key.</p>
        """.replace("{APP_NAME}", APP_NAME))
        layout.addWidget(text)
        return widget

    def create_theming_tab(self):
        """Themes and appearance tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
        <h2>Themes & Appearance</h2>
        <p><b>Secure Notepad Pro</b> supports dynamic theme switching based on your system settings 
        and allows manual overrides.</p>

        <h3>Automatic Mode</h3>
        <p>By default, the application detects your OS theme and switches automatically:</p>
        <ul>
            <li>🌓 <b>Dark Mode:</b> Activated during night hours or if your system uses a dark theme.</li>
            <li>🌕 <b>Light Mode:</b> Activated during daytime or if your system uses a light theme.</li>
        </ul>

        <h3>Manual Override</h3>
        <p>Use <b>View → Theme</b> or press <b>Ctrl + T</b> to toggle manually between themes.</p>

        <h3>Custom Styles</h3>
        <p>You can modify or replace <code>dark_theme.qss</code> or <code>light_theme.qss</code> 
        in the <code>/assets/themes/</code> directory to create your own look.</p>
        """)
        layout.addWidget(text)
        return widget

    def create_troubleshooting_tab(self):
        """Troubleshooting and support tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml(f"""
        <h2>Troubleshooting Guide</h2>

        <h3>Common Issues</h3>
        <h4>1. File Won’t Open</h4>
        <p><b>Cause:</b> Wrong password or corrupted file.<br>
        <b>Fix:</b> Ensure you are using the correct password and that the file has not been altered.</p>

        <h4>2. Theme Not Switching</h4>
        <p><b>Cause:</b> OS theme change not detected immediately.<br>
        <b>Fix:</b> Restart {APP_NAME} or manually toggle theme using <b>Ctrl + T</b>.</p>

        <h4>3. Slow Startup</h4>
        <p><b>Fix:</b> Disable heavy antivirus scanning on the installation folder.</p>

        <h3>Getting Support</h3>
        <ul>
            <li>Check the project’s GitHub page for FAQs and updates.</li>
            <li>Use “Help → About” for version and developer info.</li>
            <li>Submit bug reports with logs if persistent.</li>
        </ul>

        <p>Thank you for using <b>{APP_NAME}</b> — your privacy-focused notepad solution.</p>
        """)
        layout.addWidget(text)
        return widget
