# 🚀 Secured Notepad v2.0.0 – Major Release

We’re proud to announce **Secured Notepad Pro v2.0.0**, a professional encrypted note-taking application built with **Python** and **PyQt5**.  
Designed for developers, writers, and privacy-conscious users who value both security and simplicity.

---

## ✨ Features

### 🛡 Encryption

* AES-256-GCM encryption with HMAC-SHA256 authentication
* Secure `.txt.enc` file format
* Password-protected saving and opening dialogs
* Zero plaintext saved to disk during encryption
* Pure Python encryption backend

### 🌙 Interface

* Beautiful all-dark modern UI with high contrast readability
* **Multi-tab support** – work with multiple notes simultaneously
* Clean layout with responsive scaling
* Integrated **line numbering**, **status bar**, and **zoom controls**
* Mouse-scroll zoom supported (`Ctrl + Mouse Scroll`)
* High-DPI support for 4K and Retina displays

### ⚙ Functionality

* Real-time autosave system
* Modular structure for easy updates and maintenance
* Full **menu bar with keyboard shortcuts**
* Status bar showing: line, column, zoom, encoding, and encryption state
* Always enforced dark theme for consistent UI

---

## 🧩 Technical Overview

* **Language:** Python 3.10+
* **Framework:** PyQt5
* **Encryption:** AES-256-GCM / HMAC-SHA256
* **Supported OS:** Windows, Linux, macOS
* **File Extensions:** `.txt`, `.txt.enc`
* **Features:** Multi-tab, mouse-scroll zoom, line numbers, dark theme

---

## 🧠 Usage Guide

1. Launch `notepad.py`
2. Open or create multiple tabs with `Ctrl+T`
3. Switch tabs via `Ctrl+Tab` or click the tab headers
4. Save normally (`Ctrl + S`) or as encrypted (`Ctrl + Shift + S`)
5. Enter a strong password when saving encrypted files
6. Reopen `.txt.enc` files by entering your password to decrypt
7. Zoom in/out using `Ctrl + Mouse Scroll` or keyboard shortcuts

> 💡 Tip: Always back up your encrypted files and passwords securely.

---

## 🧯 Installation

```bash
git clone https://github.com/j3fcruz/Secured-Notepad.git
cd Secured-Notepad
python -m venv venv
# Activate venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
pip install -r requirements.txt
python notepad.py
