"""
設定パネル
Panel for application settings.
"""

from PyQt5.QtWidgets import (QGroupBox, QFormLayout, QLineEdit, QSpinBox, QLabel)
from PyQt5.QtCore import Qt
from cut_numbering_manager.config import DEFAULT_IP, DEFAULT_PORT


class SettingsPanel(QGroupBox):
    """Panel for application settings"""
    def __init__(self, parent=None):
        super().__init__("OSC設定")
        self.parent = parent
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QFormLayout()
        
        self.ip_input = QLineEdit(DEFAULT_IP)
        layout.addRow("IPアドレス:", self.ip_input)
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(DEFAULT_PORT)
        layout.addRow("ポート:", self.port_input)
        
        version_note = QLabel("OSC for OBS v2.7.1 (OBS v27.2.4用)")
        version_note.setStyleSheet("font-weight: bold;")
        layout.addRow("バージョン:", version_note)
        
        command_note = QLabel("録画コマンド: /setRecording (値: 1=開始, 0=停止)")
        command_note.setStyleSheet("color: #555; font-style: italic;")
        layout.addRow("", command_note)
        
        filename_note = QLabel("ファイル名設定コマンド: /recFileName (標準OSC形式)")
        filename_note.setStyleSheet("color: #555; font-style: italic;")
        layout.addRow("", filename_note)
        
        format_note = QLabel("※ 標準OSC形式を使用 (python-osc)")
        format_note.setStyleSheet("color: #555; font-style: italic;")
        layout.addRow("", format_note)
        
        self.setLayout(layout)
    
    def get_ip(self):
        """Get the current IP address from input"""
        return self.ip_input.text()
    
    def get_port(self):
        """Get the current port from input"""
        return self.port_input.value()
