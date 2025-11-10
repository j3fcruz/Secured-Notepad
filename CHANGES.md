# CHANGELOG

## [2.0.0] – 2025-11-10
### Major Release

#### 🚀 New Features & Improvements
- **Multi-Tab Support:** Open and manage multiple documents simultaneously.
- **Mouse-Scroll Zoom:** Zoom in/out text editor content using Ctrl + scroll or keyboard shortcuts.
- **Theme Manager:** Added `theme_manager.py` for automatic dark/light theme handling.
- **Icon Manager:** Added `icon_manager.py` to centralize icon loading and safe resource fallback.
- **High-DPI Support:** Improved UI scaling for 4K and Retina displays.
- **Always-On Dark Theme:** UI enforces consistent dark mode regardless of system settings.
- **Modular Architecture:** Refined folder structure (`/ui`, `/utils`, `/assets`) for better maintainability.
- **About Dialog:** Added professional author info with clickable icon-based buttons for website, GitHub, and Ko-fi.
- **Status Bar Enhancements:** Shows line, column, zoom level, encoding, and encryption state dynamically.

#### 🔐 Security & Backend
- AES-256-GCM encryption with HMAC-SHA256 integrity.
- Password-protected `.txt.enc` file format.
- Pure Python encryption backend (no compiled `.pyd` modules required).
- Zero plaintext saved to disk during encryption operations.

#### 🎨 UI & UX
- Refined dark theme styling with QSS fallback.
- Improved line numbering and zoom behavior.
- Polished menu bar, toolbar, and button styling for modern professional look.
- Window icon loading handled safely across platforms.

#### 🧩 Developer Experience
- Modular, maintainable codebase with simplified imports.
- Real-time autosave system.
- Prepared for standalone packaging with PyInstaller (`--onedir`, `--noconsole`, custom icon support).
- Better logging and safe error handling on startup and runtime.

---

## [1.0.0] – 2025-10-28
### Initial Stable Release
- Basic text editing, file open/save functionality.
- AES-256 encryption for `.txt.enc` files.
- Dark theme with line numbering, zoom controls, and status bar.
- High-DPI support.
- No multi-tab support.
- Encryption only available if `cryptography` module is installed.
