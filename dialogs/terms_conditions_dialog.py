# dialog/terms_conditions_dialog.py

"""
Terms and Conditions dialog for Secure Notepad Pro
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QCheckBox, QScrollArea, QWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from config.app_config import APP_NAME, APP_VERSION, APP_DEVELOPER, AUTHOR


class TermsConditionsDialog(QDialog):
    """Terms and Conditions dialog for Secure Notepad Pro"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - Terms and Conditions")
        self.setFixedSize(750, 800)
        self.setModal(True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_label = QLabel("Terms and Conditions")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Subtitle
        subtitle_label = QLabel(f"{APP_NAME} Pro - Version {APP_VERSION}")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #999aab;")
        layout.addWidget(subtitle_label)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #3d3d5c;")
        layout.addWidget(separator)

        # Terms Content
        terms_content = QTextEdit()
        terms_content.setReadOnly(True)
        terms_content.setHtml(f"""
        <div style="font-size: 12px; line-height: 1.8; color: #dcdcdc;">
            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">1. Acceptance of Terms</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">By using {APP_NAME} Pro ("Software"), you agree to comply with and be bound by these Terms and Conditions. If you do not agree with any part of these terms, please do not use the Software.</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">2. License Grant</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">{APP_NAME} Pro is provided as-is with a personal, non-exclusive, non-transferable license. You may use this Software on a single device for personal and professional purposes. Redistribution or modification without explicit permission is prohibited.</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">3. User Responsibilities</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">You are responsible for:</p>
            <ul style="margin: 8px 0 8px 20px; color: #b0b0c0;">
                <li>Maintaining the confidentiality of any encryption keys or passwords</li>
                <li>Creating regular backups of your important notes and documents</li>
                <li>Ensuring compliance with all applicable laws and regulations</li>
                <li>Using the Software for lawful purposes only</li>
            </ul>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">4. Data Security and Privacy</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">{APP_NAME} Pro employs industry-standard encryption to protect your data. However, no method of transmission or storage is completely secure. We recommend backing up your important data regularly. We do not store, monitor, or access your personal notes without your explicit consent.</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">5. Limitation of Liability</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. IN NO EVENT SHALL {APP_DEVELOPER} BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES, INCLUDING DATA LOSS OR BUSINESS INTERRUPTION.</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">6. Disclaimer of Warranties</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">We make no warranties, express or implied, regarding the Software's fitness for a particular purpose, merchantability, or non-infringement. Use at your own discretion and risk.</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">7. Prohibited Uses</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">You may not use the Software to:</p>
            <ul style="margin: 8px 0 8px 20px; color: #b0b0c0;">
                <li>Engage in illegal activities or violate any laws</li>
                <li>Harass, abuse, or threaten others</li>
                <li>Create malware or attempt unauthorized access</li>
                <li>Reverse engineer or attempt to decompile the Software</li>
                <li>Circumvent security measures or encryption</li>
            </ul>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">8. Intellectual Property</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">All intellectual property rights in {APP_NAME} Pro, including copyrights, trademarks, and patents, are owned by {APP_DEVELOPER}. You may not reproduce, distribute, or transmit the Software without explicit written permission.</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">9. Updates and Modifications</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">We reserve the right to modify, update, or discontinue the Software at any time. Changes may include feature updates, security patches, or interface improvements. You agree to accept such updates.</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">10. Termination</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">Your license to use the Software may be terminated if you violate these Terms and Conditions. Upon termination, you must cease all use and delete all copies from your devices.</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">11. Governing Law</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">These Terms and Conditions are governed by applicable laws. Any disputes shall be resolved through appropriate legal channels.</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">12. Contact Information</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">For questions or concerns about these Terms and Conditions, please contact:</p>
            <p style="margin: 8px 0; color: #b0b0c0;"><strong>Developer:</strong> {APP_DEVELOPER}<br/><strong>Author:</strong> {AUTHOR}</p>

            <h3 style="color: #6366f1; margin-top: 16px; margin-bottom: 10px; font-size: 14px;">13. Entire Agreement</h3>
            <p style="margin: 8px 0; color: #b0b0c0;">These Terms and Conditions constitute the entire agreement between you and {APP_DEVELOPER} regarding the Software and supersede all prior agreements and understandings.</p>

            <p style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #3d3d5c; color: #999aab; font-size: 11px;"><strong>Last Updated:</strong> {APP_VERSION}<br/>By using {APP_NAME} Pro, you acknowledge that you have read, understood, and agree to be bound by these Terms and Conditions.</p>
        </div>
        """)
        layout.addWidget(terms_content)

        # Acceptance Checkbox
        acceptance_layout = QHBoxLayout()
        self.accept_checkbox = QCheckBox("I have read and agree to the Terms and Conditions")
        self.accept_checkbox.setStyleSheet("""
            QCheckBox {
                color: #b0b0c0;
                spacing: 8px;
                font-size: 11px;
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
            QCheckBox::indicator:hover {
                border: 1px solid #6366f1;
            }
        """)
        acceptance_layout.addWidget(self.accept_checkbox)
        acceptance_layout.addStretch()
        layout.addLayout(acceptance_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.print_btn = QPushButton("Print")
        self.print_btn.setFixedWidth(100)
        self.print_btn.setMinimumHeight(38)
        self.print_btn.clicked.connect(self.print_terms)
        button_layout.addWidget(self.print_btn)

        button_layout.addStretch()


        #self.decline_btn = QPushButton("Decline")
        #self.decline_btn.setFixedWidth(100)
        #self.decline_btn.setMinimumHeight(38)
        #self.decline_btn.clicked.connect(self.reject)
        #button_layout.addWidget(self.decline_btn)


        self.accept_btn = QPushButton("Accept & Continue")
        self.accept_btn.setFixedWidth(150)
        self.accept_btn.setMinimumHeight(38)
        self.accept_btn.setEnabled(False)
        self.accept_btn.clicked.connect(self.accept_terms)
        self.accept_checkbox.stateChanged.connect(
            lambda: self.accept_btn.setEnabled(self.accept_checkbox.isChecked())
        )
        button_layout.addWidget(self.accept_btn)

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
                background-color: #16213e;
                color: #dcdcdc;
                border: 1px solid #3d3d5c;
                border-radius: 8px;
                padding: 15px;
                font-family: "Segoe UI", monospace;
                font-size: 12px;
                line-height: 1.6;
            }
            QTextEdit:focus {
                border: 2px solid #6366f1;
                background-color: #1a1a2e;
            }

            /* Push Button */
            QPushButton {
                background-color: #0078D4;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }

            /* Labels */
            QLabel {
                color: #dcdcdc;
                font-size: 12px;
            }

            /* Checkbox */
            QCheckBox {
                color: #b0b0c0;
                spacing: 8px;
                font-size: 11px;
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
            QCheckBox::indicator:hover {
                border: 1px solid #6366f1;
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
        """)

    def accept_terms(self):
        """Accept terms and close dialog"""
        if self.accept_checkbox.isChecked():
            self.accept()

    def print_terms(self):
        """Print terms and conditions"""
        try:
            from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
            from PyQt5.QtGui import QTextDocument

            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)

            if dialog.exec_() == QDialog.Accepted:
                doc = QTextDocument()
                doc.setHtml(self.sender().parent().findChild(QTextEdit).toHtml())
                doc.print(printer)
        except Exception as e:
            print(f"Print error: {e}")