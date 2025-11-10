"""
utils/editor.py
---------
EnhancedTextEditor with line numbers, current-line highlighting, and professional defaults.
"""

from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QPainter, QColor, QTextFormat, QFontDatabase, QFont, QWheelEvent


class LineNumberArea(QWidget):
    """Displays line numbers next to the text editor."""

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.wheel_zoom_callback = None  # callback to be set by main window

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class EnhancedTextEditor(QPlainTextEdit):
    DEFAULT_FONT_SIZE = 14

    def __init__(self):
        super().__init__()

        # --- Font Setup ---
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(self.DEFAULT_FONT_SIZE)
        self.setFont(font)

        # Tab stops = 4 spaces
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)

        # --- Line Number Area ---
        self.lineNumberArea = LineNumberArea(self)

        # --- Signals ---
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        # --- Initial setup ---
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    # ---------------- Line Number Area ----------------
    def lineNumberAreaWidth(self):
        """Calculate required width for line numbers."""
        digits = len(str(max(1, self.blockCount())))
        return 3 + self.fontMetrics().horizontalAdvance("9") * digits + 4

    def updateLineNumberAreaWidth(self, _):
        """Update the left margin to fit line numbers."""
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        """Scroll or update the line number area when editor changes."""
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def lineNumberAreaPaintEvent(self, event):
        """Paint the line numbers."""
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#222222"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor("#858585"))
                painter.drawText(
                    0, top, self.lineNumberArea.width() - 4, self.fontMetrics().height(),
                    Qt.AlignRight, str(block_number + 1)
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def resizeEvent(self, event):
        """Ensure the line number area geometry matches the editor."""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    # ---------------- Highlight Current Line ----------------
    def highlightCurrentLine(self):
        """Highlight the line where the cursor is."""
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor(45, 45, 45))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    # ---------------- Wheel Event ----------------
    def wheelEvent_old(self, event: QWheelEvent):
        """Handle mouse wheel zoom with Ctrl modifier"""
        if event.modifiers() == Qt.ControlModifier:
            # Get the parent window (EnhancedNotepad) to call zoom methods
            parent = self.parent()
            if hasattr(parent, 'zoom_in') and hasattr(parent, 'zoom_out'):
                if event.angleDelta().y() > 0:
                    parent.zoom_in()
                else:
                    parent.zoom_out()
                event.accept()
        else:
            # Let the default scroll behavior work
            super().wheelEvent(event)


    def set_wheel_zoom_callback(self, callback):
        """Set a function to call with delta (+1/-1) when Ctrl+Wheel is used."""
        self.wheel_zoom_callback = callback

    def wheelEvent(self, event):
        """Override to handle Ctrl+Wheel for zooming."""
        if event.modifiers() == Qt.ControlModifier and self.wheel_zoom_callback:
            delta = 1 if event.angleDelta().y() > 0 else -1
            self.wheel_zoom_callback(delta)
            event.accept()
        else:
            super().wheelEvent(event)