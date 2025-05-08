"""
ファイル名プレビューパネル
Panel for filename preview.
"""

from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt


class PreviewPanel(QGroupBox):
    """Panel for filename preview"""
    def __init__(self, parent=None):
        super().__init__("ファイル名プレビュー")
        self.parent = parent
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        
        self.filename_preview = QLabel()
        self.filename_preview.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.filename_preview.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.filename_preview)
        
        self.setLayout(layout)
    
    def update_preview(self, filename):
        """Update the filename preview"""
        self.filename_preview.setText(filename)
