# dialog/donate_dialog.py

"""
Donate dialog for supporting the project
"""

import webbrowser
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QGroupBox, QMessageBox, QApplication
)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
from config.app_config import CONFIG, ABOUT_APP, APP_NAME, APP_VERSION, APP_DEVELOPER, AUTHOR, HASH_NAME


class DonateDialog(QDialog):
    """Donate dialog for supporting the project"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Support {APP_NAME}")
        self.setFixedSize(600, 700)
        self.setModal(True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_label = QLabel(f"Support {APP_NAME}")
        header_font = QFont()
        header_font.setPointSize(25)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Subtitle
        subtitle_label = QLabel("Help us continue improving this tool for the community")
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

        # Description
        description = QTextEdit()
        description.setReadOnly(True)
        description.setMaximumHeight(140)
        description.setHtml(f"""
        <div style="font-size: 13px; line-height: 1.6;">
            <p style="margin: 0 0 12px 0; color: #dcdcdc;"><strong>Why Support Us?</strong></p>
            <p style="margin: 0; color: #b0b0c0;">{APP_NAME} is developed with passion and dedication. Your support helps us:</p>
            <ul style="margin: 8px 0 0 20px; color: #b0b0c0; line-height: 1.8;">
                <li>Continue developing innovative features</li>
                <li>Maintain compatibility with latest Python versions</li>
                <li>Provide comprehensive documentation and support</li>
                <li>Keep the software free and open source</li>
            </ul>
        </div>
        """)
        layout.addWidget(description)

        # Donation options
        donation_group = QGroupBox("Ways to Support")
        donation_layout = QVBoxLayout(donation_group)
        donation_layout.setSpacing(12)

        # GitHub Sponsors
        github_layout = QHBoxLayout()
        github_icon = QLabel("⭐")
        github_icon_font = QFont()
        github_icon_font.setPointSize(14)
        github_icon.setFont(github_icon_font)
        github_label = QLabel("Star us on GitHub")
        github_label_sub = QLabel("Follow our project and show your support")
        github_label_sub.setStyleSheet("color: #999aab; font-size: 10px;")
        github_label_sub.setMaximumHeight(16)

        github_text_layout = QVBoxLayout()
        github_text_layout.setSpacing(2)
        github_label_font = QFont()
        github_label_font.setPointSize(12)
        github_label_font.setBold(True)
        github_label.setFont(github_label_font)
        github_text_layout.addWidget(github_label)
        github_text_layout.addWidget(github_label_sub)

        github_btn = QPushButton("Visit GitHub")
        github_btn.setFixedWidth(135)
        github_btn.setFixedHeight(36)
        github_btn.clicked.connect(lambda: webbrowser.open(CONFIG["GITHUB_ID"]))

        github_layout.addWidget(github_icon)
        github_layout.addLayout(github_text_layout)
        github_layout.addStretch()
        github_layout.addWidget(github_btn)
        donation_layout.addLayout(github_layout)

        # PayPal
        paypal_layout = QHBoxLayout()
        paypal_icon = QLabel("💳")
        paypal_icon_font = QFont()
        paypal_icon_font.setPointSize(14)
        paypal_icon.setFont(paypal_icon_font)
        paypal_label = QLabel("Donate via PayPal")
        paypal_label_sub = QLabel("Secure and convenient payment option")
        paypal_label_sub.setStyleSheet("color: #999aab; font-size: 10px;")
        paypal_label_sub.setMaximumHeight(16)

        paypal_text_layout = QVBoxLayout()
        paypal_text_layout.setSpacing(2)
        paypal_label_font = QFont()
        paypal_label_font.setPointSize(12)
        paypal_label_font.setBold(True)
        paypal_label.setFont(paypal_label_font)
        paypal_text_layout.addWidget(paypal_label)
        paypal_text_layout.addWidget(paypal_label_sub)

        paypal_btn = QPushButton("Donate Now")
        paypal_btn.setFixedWidth(135)
        paypal_btn.setFixedHeight(36)
        paypal_btn.clicked.connect(lambda: webbrowser.open(CONFIG["PAYPAL_ID"]))

        paypal_layout.addWidget(paypal_icon)
        paypal_layout.addLayout(paypal_text_layout)
        paypal_layout.addStretch()
        paypal_layout.addWidget(paypal_btn)
        donation_layout.addLayout(paypal_layout)

        # Ko-fi
        kofi_layout = QHBoxLayout()
        kofi_icon = QLabel("☕")
        kofi_icon_font = QFont()
        kofi_icon_font.setPointSize(14)
        kofi_icon.setFont(kofi_icon_font)
        kofi_label = QLabel("Buy us a Coffee")
        kofi_label_sub = QLabel("Support with any amount you choose")
        kofi_label_sub.setStyleSheet("color: #999aab; font-size: 10px;")
        kofi_label_sub.setMaximumHeight(16)

        kofi_text_layout = QVBoxLayout()
        kofi_text_layout.setSpacing(2)
        kofi_label_font = QFont()
        kofi_label_font.setPointSize(12)
        kofi_label_font.setBold(True)
        kofi_label.setFont(kofi_label_font)
        kofi_text_layout.addWidget(kofi_label)
        kofi_text_layout.addWidget(kofi_label_sub)

        kofi_btn = QPushButton("Ko-fi")
        kofi_btn.setFixedWidth(135)
        kofi_btn.setFixedHeight(36)
        kofi_btn.clicked.connect(lambda: webbrowser.open(CONFIG["KOFI_ID"]))

        kofi_layout.addWidget(kofi_icon)
        kofi_layout.addLayout(kofi_text_layout)
        kofi_layout.addStretch()
        kofi_layout.addWidget(kofi_btn)
        donation_layout.addLayout(kofi_layout)

        # Crypto
        crypto_layout = QHBoxLayout()
        crypto_icon = QLabel("🪙")
        crypto_icon_font = QFont()
        crypto_icon_font.setPointSize(14)
        crypto_icon.setFont(crypto_icon_font)
        crypto_label = QLabel("Cryptocurrency")
        crypto_label_sub = QLabel("Bitcoin, Ethereum, and other cryptocurrencies")
        crypto_label_sub.setStyleSheet("color: #999aab; font-size: 10px;")
        crypto_label_sub.setMaximumHeight(16)

        crypto_text_layout = QVBoxLayout()
        crypto_text_layout.setSpacing(2)
        crypto_label_font = QFont()
        crypto_label_font.setPointSize(12)
        crypto_label_font.setBold(True)
        crypto_label.setFont(crypto_label_font)
        crypto_text_layout.addWidget(crypto_label)
        crypto_text_layout.addWidget(crypto_label_sub)

        crypto_btn = QPushButton("View Addresses")
        crypto_btn.setFixedWidth(135)
        crypto_btn.setFixedHeight(36)
        crypto_btn.clicked.connect(self.show_crypto_addresses)

        crypto_layout.addWidget(crypto_icon)
        crypto_layout.addLayout(crypto_text_layout)
        crypto_layout.addStretch()
        crypto_layout.addWidget(crypto_btn)
        donation_layout.addLayout(crypto_layout)

        layout.addWidget(donation_group)

        # Thank you message
        thanks_label = QLabel()
        thanks_label.setWordWrap(True)
        thanks_label.setText(
            f"Thank you for considering supporting {APP_NAME}! Every contribution, no matter how small, "
            "helps us continue developing and improving this tool for the Python community. Your support "
            "motivates us to deliver excellence."
        )
        thanks_label.setStyleSheet(
            "color: #999aab; font-style: italic; padding: 12px; background-color: #16213e; border-radius: 6px; border-left: 4px solid #6366f1;")
        thanks_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(thanks_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        share_btn = QPushButton("Share with Friends")
        share_btn.setMinimumHeight(38)
        share_btn.clicked.connect(self.share_application)
        button_layout.addWidget(share_btn)

        button_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(100)
        close_btn.setMinimumHeight(38)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

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
                padding: 12px;
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

            /* Labels */
            QLabel {
                color: #dcdcdc;
                font-size: 12px;
            }

            /* Group Box */
            QGroupBox {
                color: #dcdcdc;
                border: 2px solid #3d3d5c;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                padding-left: 12px;
                padding-right: 12px;
                padding-bottom: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 6px 0 6px;
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

    def show_crypto_addresses(self):
        """Show cryptocurrency addresses with copy support"""
        addresses = {
            "Bitcoin (BTC)": {CONFIG["BTC_ID"]},
            "Ethereum (ETH)": {CONFIG["ETH_ID"]}
        }

        msg = ""
        for name, address in addresses.items():
            msg += f"{name}:\n{address}\n\n"

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Crypto Addresses")
        msg_box.setText(msg.strip())
        msg_box.setFont(QFont("Segoe UI", 11))

        copy_btn = QPushButton("Copy All")
        msg_box.addButton(copy_btn, QMessageBox.ActionRole)
        msg_box.addButton(QMessageBox.Ok)

        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(msg.strip()))
        msg_box.exec_()

    def share_application(self):
        """Display sharing options in a message box with copy support."""
        share_text = (
            f"Help spread the word about {APP_NAME}!\n\n"
            "Share on social media:\n"
            f"• Twitter: Tweet using #{HASH_NAME}\n"
            "• LinkedIn: Share with your professional network\n"
            "• Reddit: Post in r/Python\n"
            "• Discord: Share in Python-related communities\n\n"
            "Tell your colleagues and friends about this free tool!"
        )

        box = QMessageBox(self)
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle(f"Share {APP_NAME}")
        box.setText(share_text)
        box.setFont(QFont("Segoe UI", 11))

        copy_button = QPushButton("Copy")
        box.addButton(copy_button, QMessageBox.ActionRole)
        box.addButton(QMessageBox.Ok)

        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(share_text))
        box.exec_()