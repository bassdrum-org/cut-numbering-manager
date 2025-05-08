"""
カット情報パネル
Panel for cut information input.
"""

from PyQt5.QtWidgets import (QGroupBox, QFormLayout, QLineEdit, QSpinBox, QHBoxLayout, QLabel, QWidget)
from cut_numbering_manager.config import (
    DEFAULT_PART_NAME, 
    DEFAULT_SCENE_NAME, 
    DEFAULT_CUT_NUMBER, 
    DEFAULT_VERSION
)
from cut_numbering_manager.models.filename_config import FilenameConfig


class CutInfoPanel(QGroupBox):
    """Panel for cut information input"""
    def __init__(self, cut_info, callback):
        super().__init__("カット情報")
        self.cut_info = cut_info
        self.callback = callback
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QFormLayout()
        
        self.part_input = QLineEdit(self.cut_info.part_name)
        layout.addRow("パート名:", self.part_input)
        self.part_input.textChanged.connect(self._on_input_changed)
        
        self.scene_input = QLineEdit(self.cut_info.scene_name)
        layout.addRow("シーン名:", self.scene_input)
        self.scene_input.textChanged.connect(self._on_input_changed)
        
        cut_container = QWidget()
        cut_layout = QHBoxLayout(cut_container)
        cut_layout.setContentsMargins(0, 0, 0, 0)
        
        self.cut_prefix_input = QLineEdit(self.cut_info.filename_config.get_prefix(FilenameConfig.CUT))
        self.cut_prefix_input.setPlaceholderText("接頭辞")
        self.cut_prefix_input.setMaximumWidth(80)
        self.cut_prefix_input.textChanged.connect(self._on_input_changed)
        cut_layout.addWidget(self.cut_prefix_input)
        
        self.cut_number_input = QSpinBox()
        self.cut_number_input.setRange(1, 9999)
        self.cut_number_input.setValue(self.cut_info.cut_number)
        self.cut_number_input.valueChanged.connect(self._on_input_changed)
        cut_layout.addWidget(self.cut_number_input)
        
        layout.addRow("カット番号:", cut_container)
        
        version_container = QWidget()
        version_layout = QHBoxLayout(version_container)
        version_layout.setContentsMargins(0, 0, 0, 0)
        
        self.version_prefix_input = QLineEdit(self.cut_info.filename_config.get_prefix(FilenameConfig.VERSION))
        self.version_prefix_input.setPlaceholderText("接頭辞")
        self.version_prefix_input.setMaximumWidth(80)
        self.version_prefix_input.textChanged.connect(self._on_input_changed)
        version_layout.addWidget(self.version_prefix_input)
        
        self.version_input = QSpinBox()
        self.version_input.setRange(1, 999)
        self.version_input.setValue(self.cut_info.version)
        self.version_input.valueChanged.connect(self._on_input_changed)
        version_layout.addWidget(self.version_input)
        
        layout.addRow("バージョン:", version_container)
        
        prefix_note = QLabel("※ 接頭辞を変更すると、ファイル名の表示形式が変わります")
        prefix_note.setStyleSheet("color: #888888; font-style: italic; font-size: 10px;")
        layout.addRow("", prefix_note)
        
        self.setLayout(layout)
    
    def _on_input_changed(self):
        """Handle input changes and update the model"""
        self.cut_info.part_name = self.part_input.text()
        self.cut_info.scene_name = self.scene_input.text()
        self.cut_info.cut_number = self.cut_number_input.value()
        self.cut_info.version = self.version_input.value()
        
        prefixes = self.cut_info.filename_config.get_all_prefixes().copy()
        prefixes[FilenameConfig.CUT] = self.cut_prefix_input.text()
        prefixes[FilenameConfig.VERSION] = self.version_prefix_input.text()
        self.cut_info.filename_config.set_all_prefixes(prefixes)
        
        if self.callback:
            self.callback()
    
    def update_ui_from_model(self):
        """Update UI components from the model"""
        self.part_input.setText(self.cut_info.part_name)
        self.scene_input.setText(self.cut_info.scene_name)
        self.cut_number_input.setValue(self.cut_info.cut_number)
        self.version_input.setValue(self.cut_info.version)
        
        prefixes = self.cut_info.filename_config.get_all_prefixes()
        self.cut_prefix_input.setText(prefixes.get(FilenameConfig.CUT, ""))
        self.version_prefix_input.setText(prefixes.get(FilenameConfig.VERSION, ""))
