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
        main_layout = QHBoxLayout()  # 水平レイアウトに変更
        self.setStyleSheet("""
            QGroupBox {
                background-color: #1a1a1a;
                border: 2px solid #ffd900;
                border-radius: 8px;
                margin-top: 0px;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Arial', 'Helvetica', sans-serif;
            }
        """)
        
        labels_layout = QVBoxLayout()
        labels_layout.setSpacing(20)
        labels_layout.setContentsMargins(10, 10, 10, 10)
        
        part_title = QLabel("パート")
        part_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        part_title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        scene_title = QLabel("シーン")
        scene_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        scene_title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        cut_title = QLabel("カット")
        cut_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        cut_title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        version_title = QLabel("バージョン")
        version_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        version_title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        labels_layout.addWidget(part_title)
        labels_layout.addWidget(scene_title)
        labels_layout.addWidget(cut_title)
        labels_layout.addWidget(version_title)
        
        values_layout = QVBoxLayout()
        values_layout.setSpacing(20)
        values_layout.setContentsMargins(10, 10, 10, 10)
        
        self.part_value = QLabel(self.cut_info.part_name)
        self.part_value.setStyleSheet("font-size: 36px; font-weight: bold;")
        self.part_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.scene_value = QLabel(self.cut_info.scene_name)
        self.scene_value.setStyleSheet("font-size: 36px; font-weight: bold;")
        self.scene_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.cut_value = QLabel(self.cut_info.get_formatted_cut_number())
        self.cut_value.setStyleSheet("font-size: 72px; font-weight: bold;")
        self.cut_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.version_value = QLabel(self.cut_info.get_formatted_version())
        self.version_value.setStyleSheet("font-size: 36px; font-weight: bold;")
        self.version_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        values_layout.addWidget(self.part_value)
        values_layout.addWidget(self.scene_value)
        values_layout.addWidget(self.cut_value)
        values_layout.addWidget(self.version_value)
        
        main_layout.addLayout(labels_layout, 1)  # 1の比率
        main_layout.addLayout(values_layout, 3)  # 3の比率（右側を大きく）
        
        self.setLayout(main_layout)
        
        self.setMinimumHeight(300)
    
    def update_ui_from_model(self):
        """Update UI components from the model"""
        self.part_value.setText(self.cut_info.part_name)
        self.scene_value.setText(self.cut_info.scene_name)
        self.cut_value.setText(self.cut_info.get_formatted_cut_number())
        self.version_value.setText(self.cut_info.get_formatted_version())
