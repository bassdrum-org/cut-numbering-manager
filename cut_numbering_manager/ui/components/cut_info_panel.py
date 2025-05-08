"""
カット情報パネル
Panel for cut information input.
"""

from PyQt5.QtWidgets import (QGroupBox, QFormLayout, QLineEdit, QSpinBox)
from cut_numbering_manager.config import (
    DEFAULT_PART_NAME, 
    DEFAULT_SCENE_NAME, 
    DEFAULT_CUT_NUMBER, 
    DEFAULT_VERSION
)


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
        
        self.cut_number_input = QSpinBox()
        self.cut_number_input.setRange(1, 9999)
        self.cut_number_input.setValue(self.cut_info.cut_number)
        layout.addRow("カット番号:", self.cut_number_input)
        self.cut_number_input.valueChanged.connect(self._on_input_changed)
        
        self.version_input = QSpinBox()
        self.version_input.setRange(1, 999)
        self.version_input.setValue(self.cut_info.version)
        layout.addRow("バージョン:", self.version_input)
        self.version_input.valueChanged.connect(self._on_input_changed)
        
        self.setLayout(layout)
    
    def _on_input_changed(self):
        """Handle input changes and update the model"""
        self.cut_info.part_name = self.part_input.text()
        self.cut_info.scene_name = self.scene_input.text()
        self.cut_info.cut_number = self.cut_number_input.value()
        self.cut_info.version = self.version_input.value()
        
        if self.callback:
            self.callback()
    
    def update_ui_from_model(self):
        """Update UI components from the model"""
        self.part_input.setText(self.cut_info.part_name)
        self.scene_input.setText(self.cut_info.scene_name)
        self.cut_number_input.setValue(self.cut_info.cut_number)
        self.version_input.setValue(self.cut_info.version)
