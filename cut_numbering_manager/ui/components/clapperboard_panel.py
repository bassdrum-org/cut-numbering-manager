"""
カチンコ（クラッパーボード）パネル
Panel for displaying cut information in a clapperboard-like UI.
"""

from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGridLayout, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QEvent
from PyQt5.QtGui import QFont, QColor


class ClapperboardPanel(QGroupBox):
    """Panel for displaying cut information in a clapperboard-like UI"""
    def __init__(self, cut_info, parent=None):
        super().__init__()
        self.setTitle("")  # タイトルは不要
        self.cut_info = cut_info
        self.parent = parent
        self.recording = False
        self.base_font_sizes = {
            'part_title': 16,
            'part_value': 42,
            'scene_title': 16,
            'scene_value': 42,
            'cut_title': 16,
            'cut_value': 84,
            'version_title': 16,
            'version_value': 42
        }
        self._init_ui()
        self.installEventFilter(self)
    
    def _init_ui(self):
        """Initialize the UI components"""
        main_layout = QVBoxLayout()
        self.setStyleSheet("""
            QGroupBox {
                background-color: #1a1a1a;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                margin-top: 0px;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Inter', 'Noto Sans', 'Arial', 'Helvetica', sans-serif;
            }
        """)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        part_container = QWidget()
        part_layout = QVBoxLayout(part_container)
        part_layout.setContentsMargins(10, 10, 10, 10)
        
        self.part_title = QLabel("パート")
        self.part_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        self.part_title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        part_layout.addWidget(self.part_title)
        
        self.part_value = QLabel(self.cut_info.part_name)
        self.part_value.setStyleSheet("font-size: 42px; font-weight: bold;")
        self.part_value.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.part_value.setWordWrap(True)  # テキストの折り返しを有効化
        self.part_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # サイズポリシーを設定
        self.part_value.setMinimumWidth(100)  # 最小幅を設定して折り返しを強制
        part_layout.addWidget(self.part_value, 1)
        
        scene_container = QWidget()
        scene_layout = QVBoxLayout(scene_container)
        scene_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scene_title = QLabel("シーン")
        self.scene_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        self.scene_title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        scene_layout.addWidget(self.scene_title)
        
        self.scene_value = QLabel(self.cut_info.scene_name)
        self.scene_value.setStyleSheet("font-size: 42px; font-weight: bold;")
        self.scene_value.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.scene_value.setWordWrap(True)  # テキストの折り返しを有効化
        self.scene_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # サイズポリシーを設定
        self.scene_value.setMinimumWidth(100)  # 最小幅を設定して折り返しを強制
        scene_layout.addWidget(self.scene_value, 1)
        
        cut_container = QWidget()
        cut_layout = QVBoxLayout(cut_container)
        cut_layout.setContentsMargins(10, 10, 10, 10)
        
        self.cut_title = QLabel("カット")
        self.cut_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        self.cut_title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        cut_layout.addWidget(self.cut_title)
        
        self.cut_value = QLabel(self.cut_info.get_formatted_cut_number())
        self.cut_value.setStyleSheet("font-size: 84px; font-weight: bold;")
        self.cut_value.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.cut_value.setWordWrap(True)  # テキストの折り返しを有効化
        self.cut_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # サイズポリシーを設定
        self.cut_value.setMinimumWidth(100)  # 最小幅を設定して折り返しを強制
        cut_layout.addWidget(self.cut_value, 1)
        
        version_container = QWidget()
        version_layout = QVBoxLayout(version_container)
        version_layout.setContentsMargins(10, 10, 10, 10)
        
        self.version_title = QLabel("バージョン")
        self.version_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        self.version_title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        version_layout.addWidget(self.version_title)
        
        self.version_value = QLabel(self.cut_info.get_formatted_version())
        self.version_value.setStyleSheet("font-size: 42px; font-weight: bold;")
        self.version_value.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.version_value.setWordWrap(True)  # テキストの折り返しを有効化
        self.version_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # サイズポリシーを設定
        self.version_value.setMinimumWidth(100)  # 最小幅を設定して折り返しを強制
        version_layout.addWidget(self.version_value, 1)
        
        grid_layout.addWidget(part_container, 0, 0)
        grid_layout.addWidget(scene_container, 0, 1)
        grid_layout.addWidget(cut_container, 1, 0)
        grid_layout.addWidget(version_container, 1, 1)
        
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)
        
        self.setMinimumHeight(350)
        
        self.update_font_sizes()
    
    def update_ui_from_model(self):
        """Update UI components from the model"""
        self.part_value.setText(self.cut_info.part_name)
        self.scene_value.setText(self.cut_info.scene_name)
        self.cut_value.setText(self.cut_info.get_formatted_cut_number())
        self.version_value.setText(self.cut_info.get_formatted_version())
        
    def eventFilter(self, obj, event):
        """Filter events to handle resize events"""
        if obj is self and event.type() == QEvent.Resize:
            self.update_font_sizes()
        return super().eventFilter(obj, event)
    
    def update_font_sizes(self):
        """Update font sizes based on current panel size"""
        width = self.width()
        height = self.height()
        
        base_width = 600
        base_height = 350
        
        scale_w = width / base_width
        scale_h = height / base_height
        scale = min(scale_w, scale_h)
        
        scale = max(scale, 0.7)
        
        min_title_size = 12
        min_value_size = 24
        min_cut_value_size = 42
        
        part_title_size = max(int(self.base_font_sizes['part_title'] * scale), min_title_size)
        part_value_size = max(int(self.base_font_sizes['part_value'] * scale), min_value_size)
        scene_title_size = max(int(self.base_font_sizes['scene_title'] * scale), min_title_size)
        scene_value_size = max(int(self.base_font_sizes['scene_value'] * scale), min_value_size)
        cut_title_size = max(int(self.base_font_sizes['cut_title'] * scale), min_title_size)
        cut_value_size = max(int(self.base_font_sizes['cut_value'] * scale), min_cut_value_size)
        version_title_size = max(int(self.base_font_sizes['version_title'] * scale), min_title_size)
        version_value_size = max(int(self.base_font_sizes['version_value'] * scale), min_value_size)
        
        self.part_title.setStyleSheet(f"color: #ffd900; font-size: {part_title_size}px; font-weight: bold;")
        self.part_value.setStyleSheet(f"font-size: {part_value_size}px; font-weight: bold;")
        self.scene_title.setStyleSheet(f"color: #ffd900; font-size: {scene_title_size}px; font-weight: bold;")
        self.scene_value.setStyleSheet(f"font-size: {scene_value_size}px; font-weight: bold;")
        self.cut_title.setStyleSheet(f"color: #ffd900; font-size: {cut_title_size}px; font-weight: bold;")
        self.cut_value.setStyleSheet(f"font-size: {cut_value_size}px; font-weight: bold;")
        self.version_title.setStyleSheet(f"color: #ffd900; font-size: {version_title_size}px; font-weight: bold;")
        self.version_value.setStyleSheet(f"font-size: {version_value_size}px; font-weight: bold;")
    
    def set_recording(self, is_recording):
        """Set recording state and update UI accordingly"""
        self.recording = is_recording
        
        if hasattr(self, 'breathing_animation'):
            self.breathing_animation.stop()
        
        if is_recording:
            self.setStyleSheet("""
                QGroupBox {
                    background-color: #1a1a1a;
                    border: 2px solid #ffd900;
                    border-radius: 5px;
                    margin-top: 0px;
                }
                QLabel {
                    color: #ffffff;
                    font-family: 'Inter', 'Noto Sans', 'Arial', 'Helvetica', sans-serif;
                }
            """)
        else:
            self.setStyleSheet("""
                QGroupBox {
                    background-color: #1a1a1a;
                    border: 1px solid #3a3a3a;
                    border-radius: 5px;
                    margin-top: 0px;
                }
                QLabel {
                    color: #ffffff;
                    font-family: 'Inter', 'Noto Sans', 'Arial', 'Helvetica', sans-serif;
                }
            """)
