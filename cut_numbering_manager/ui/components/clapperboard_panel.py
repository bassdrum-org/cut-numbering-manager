"""
カチンコ（クラッパーボード）パネル
Panel for displaying cut information in a clapperboard-like UI.
"""

from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ClapperboardPanel(QGroupBox):
    """Panel for displaying cut information in a clapperboard-like UI"""
    def __init__(self, cut_info, parent=None):
        super().__init__()
        self.setTitle("")  # タイトルは不要
        self.cut_info = cut_info
        self.parent = parent
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        main_layout = QVBoxLayout()
        self.setStyleSheet("""
            QGroupBox {
                background-color: #1a1a1a;
                border: 2px solid #ffd900;
                border-radius: 8px;
                margin-top: 0px;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Courier New', monospace;
            }
        """)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        part_title = QLabel("パート")
        part_title.setStyleSheet("color: #ffd900; font-size: 14px; font-weight: bold;")
        part_title.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(part_title, 0, 0)
        
        self.part_value = QLabel(self.cut_info.part_name)
        self.part_value.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.part_value.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.part_value, 1, 0)
        
        scene_title = QLabel("シーン")
        scene_title.setStyleSheet("color: #ffd900; font-size: 14px; font-weight: bold;")
        scene_title.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(scene_title, 0, 1)
        
        self.scene_value = QLabel(self.cut_info.scene_name)
        self.scene_value.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.scene_value.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.scene_value, 1, 1)
        
        cut_title = QLabel("カット")
        cut_title.setStyleSheet("color: #ffd900; font-size: 14px; font-weight: bold;")
        cut_title.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(cut_title, 2, 0)
        
        self.cut_value = QLabel(self.cut_info.get_formatted_cut_number())
        self.cut_value.setStyleSheet("font-size: 64px; font-weight: bold;")
        self.cut_value.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.cut_value, 3, 0)
        
        version_title = QLabel("バージョン")
        version_title.setStyleSheet("color: #ffd900; font-size: 14px; font-weight: bold;")
        version_title.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(version_title, 2, 1)
        
        self.version_value = QLabel(self.cut_info.get_formatted_version())
        self.version_value.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.version_value.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.version_value, 3, 1)
        
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)
        
        self.setMinimumHeight(250)
    
    def update_ui_from_model(self):
        """Update UI components from the model"""
        self.part_value.setText(self.cut_info.part_name)
        self.scene_value.setText(self.cut_info.scene_name)
        self.cut_value.setText(self.cut_info.get_formatted_cut_number())
        self.version_value.setText(self.cut_info.get_formatted_version())
