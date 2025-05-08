"""
カチンコ（クラッパーボード）パネル
Panel for displaying cut information in a clapperboard-like UI.
"""

from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGridLayout)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QColor


class ClapperboardPanel(QGroupBox):
    """Panel for displaying cut information in a clapperboard-like UI"""
    def __init__(self, cut_info, parent=None):
        super().__init__()
        self.setTitle("")  # タイトルは不要
        self.cut_info = cut_info
        self.parent = parent
        self.recording = False
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
                font-family: 'Inter', 'Noto Sans', 'Arial', 'Helvetica', sans-serif;
            }
        """)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        part_container = QWidget()
        part_layout = QHBoxLayout(part_container)
        part_layout.setContentsMargins(5, 5, 5, 5)
        
        part_title = QLabel("パート")
        part_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        part_title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        part_layout.addWidget(part_title)
        
        self.part_value = QLabel(self.cut_info.part_name)
        self.part_value.setStyleSheet("font-size: 42px; font-weight: bold;")
        self.part_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        part_layout.addWidget(self.part_value, 1)
        
        scene_container = QWidget()
        scene_layout = QHBoxLayout(scene_container)
        scene_layout.setContentsMargins(5, 5, 5, 5)
        
        scene_title = QLabel("シーン")
        scene_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        scene_title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        scene_layout.addWidget(scene_title)
        
        self.scene_value = QLabel(self.cut_info.scene_name)
        self.scene_value.setStyleSheet("font-size: 42px; font-weight: bold;")
        self.scene_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        scene_layout.addWidget(self.scene_value, 1)
        
        cut_container = QWidget()
        cut_layout = QHBoxLayout(cut_container)
        cut_layout.setContentsMargins(5, 5, 5, 5)
        
        cut_title = QLabel("カット")
        cut_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        cut_title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        cut_layout.addWidget(cut_title)
        
        self.cut_value = QLabel(self.cut_info.get_formatted_cut_number())
        self.cut_value.setStyleSheet("font-size: 84px; font-weight: bold;")
        self.cut_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        cut_layout.addWidget(self.cut_value, 1)
        
        version_container = QWidget()
        version_layout = QHBoxLayout(version_container)
        version_layout.setContentsMargins(5, 5, 5, 5)
        
        version_title = QLabel("バージョン")
        version_title.setStyleSheet("color: #ffd900; font-size: 16px; font-weight: bold;")
        version_title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        version_layout.addWidget(version_title)
        
        self.version_value = QLabel(self.cut_info.get_formatted_version())
        self.version_value.setStyleSheet("font-size: 42px; font-weight: bold;")
        self.version_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        version_layout.addWidget(self.version_value, 1)
        
        grid_layout.addWidget(part_container, 0, 0)
        grid_layout.addWidget(scene_container, 0, 1)
        grid_layout.addWidget(cut_container, 1, 0)
        grid_layout.addWidget(version_container, 1, 1)
        
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)
        
        self.setMinimumHeight(350)
    
    def update_ui_from_model(self):
        """Update UI components from the model"""
        self.part_value.setText(self.cut_info.part_name)
        self.scene_value.setText(self.cut_info.scene_name)
        self.cut_value.setText(self.cut_info.get_formatted_cut_number())
        self.version_value.setText(self.cut_info.get_formatted_version())
    
    def set_recording(self, is_recording):
        """Set recording state and update UI accordingly"""
        self.recording = is_recording
        
        if hasattr(self, 'breathing_animation'):
            self.breathing_animation.stop()
        
        if is_recording:
            self.breathing_animation = QPropertyAnimation(self, b"styleSheet")
            self.breathing_animation.setDuration(1500)  # 1.5秒周期
            self.breathing_animation.setStartValue("""
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
            self.breathing_animation.setEndValue("""
                QGroupBox {
                    background-color: #1a1a1a;
                    border: 2px solid #ff0000;
                    border-radius: 8px;
                    margin-top: 0px;
                }
                QLabel {
                    color: #ffffff;
                    font-family: 'Arial', 'Helvetica', sans-serif;
                }
            """)
            self.breathing_animation.setLoopCount(-1)  # 無限ループ
            self.breathing_animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.breathing_animation.start()
        else:
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
