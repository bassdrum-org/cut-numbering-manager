"""
設定パネル
Panel for application settings.
"""

from PyQt5.QtWidgets import (QGroupBox, QFormLayout, QLineEdit, QSpinBox, QLabel, 
                            QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, 
                            QListWidgetItem, QWidget, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from cut_numbering_manager.config import DEFAULT_IP, DEFAULT_PORT
from cut_numbering_manager.models.filename_config import FilenameConfig


class SettingsPanel(QWidget):
    """Panel for application settings"""
    
    filename_order_changed = pyqtSignal(list)
    prefix_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.filename_config = FilenameConfig()
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        main_layout = QVBoxLayout()
        
        osc_group = QGroupBox("OSC設定")
        osc_layout = QFormLayout()
        
        self.ip_input = QLineEdit(DEFAULT_IP)
        osc_layout.addRow("IPアドレス:", self.ip_input)
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(DEFAULT_PORT)
        osc_layout.addRow("ポート:", self.port_input)
        
        version_note = QLabel("OSC for OBS v2.7.1 (OBS v27.2.4用)")
        version_note.setStyleSheet("font-weight: bold;")
        osc_layout.addRow("バージョン:", version_note)
        
        command_note = QLabel("録画コマンド: /setRecording (値: 1=開始, 0=停止)")
        command_note.setStyleSheet("color: #555; font-style: italic;")
        osc_layout.addRow("", command_note)
        
        filename_note = QLabel("ファイル名設定コマンド: /recFileName (標準OSC形式)")
        filename_note.setStyleSheet("color: #555; font-style: italic;")
        osc_layout.addRow("", filename_note)
        
        format_note = QLabel("※ 標準OSC形式を使用 (python-osc)")
        format_note.setStyleSheet("color: #555; font-style: italic;")
        osc_layout.addRow("", format_note)
        
        osc_group.setLayout(osc_layout)
        main_layout.addWidget(osc_group)
        
        filename_group = QGroupBox("ファイル名設定")
        filename_layout = QVBoxLayout()
        
        order_label = QLabel("要素順序")
        order_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        filename_layout.addWidget(order_label)
        
        filename_desc = QLabel("ファイル名の要素順序を変更できます。上下ボタンで順序を変更してください。")
        filename_desc.setWordWrap(True)
        filename_layout.addWidget(filename_desc)
        
        self.element_list = QListWidget()
        self.update_element_list()
        filename_layout.addWidget(self.element_list)
        
        buttons_layout = QHBoxLayout()
        
        self.up_button = QPushButton("↑ 上へ")
        self.up_button.clicked.connect(self.move_element_up)
        buttons_layout.addWidget(self.up_button)
        
        self.down_button = QPushButton("↓ 下へ")
        self.down_button.clicked.connect(self.move_element_down)
        buttons_layout.addWidget(self.down_button)
        
        self.reset_order_button = QPushButton("デフォルト順序に戻す")
        self.reset_order_button.clicked.connect(self.reset_element_order)
        buttons_layout.addWidget(self.reset_order_button)
        
        filename_layout.addLayout(buttons_layout)
        
        prefix_label = QLabel("接頭辞設定")
        prefix_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        filename_layout.addWidget(prefix_label)
        
        prefix_desc = QLabel("各要素の接頭辞を設定できます。空欄の場合はデフォルト値が使用されます。")
        prefix_desc.setWordWrap(True)
        filename_layout.addWidget(prefix_desc)
        
        prefix_grid = QGridLayout()
        
        prefix_grid.addWidget(QLabel("パート:"), 0, 0)
        self.part_prefix_input = QLineEdit(self.filename_config.get_prefix(FilenameConfig.PART))
        self.part_prefix_input.setPlaceholderText("接頭辞なし")
        self.part_prefix_input.textChanged.connect(self.update_prefix)
        prefix_grid.addWidget(self.part_prefix_input, 0, 1)
        
        prefix_grid.addWidget(QLabel("シーン:"), 1, 0)
        self.scene_prefix_input = QLineEdit(self.filename_config.get_prefix(FilenameConfig.SCENE))
        self.scene_prefix_input.setPlaceholderText("接頭辞なし")
        self.scene_prefix_input.textChanged.connect(self.update_prefix)
        prefix_grid.addWidget(self.scene_prefix_input, 1, 1)
        
        prefix_grid.addWidget(QLabel("カット:"), 2, 0)
        self.cut_prefix_input = QLineEdit(self.filename_config.get_prefix(FilenameConfig.CUT))
        self.cut_prefix_input.setPlaceholderText("接頭辞なし")
        self.cut_prefix_input.textChanged.connect(self.update_prefix)
        prefix_grid.addWidget(self.cut_prefix_input, 2, 1)
        
        prefix_grid.addWidget(QLabel("バージョン:"), 3, 0)
        self.version_prefix_input = QLineEdit(self.filename_config.get_prefix(FilenameConfig.VERSION))
        self.version_prefix_input.setPlaceholderText("v")
        self.version_prefix_input.textChanged.connect(self.update_prefix)
        prefix_grid.addWidget(self.version_prefix_input, 3, 1)
        
        filename_layout.addLayout(prefix_grid)
        
        self.reset_prefix_button = QPushButton("デフォルト接頭辞に戻す")
        self.reset_prefix_button.clicked.connect(self.reset_prefixes)
        filename_layout.addWidget(self.reset_prefix_button)
        
        preview_label = QLabel("プレビュー: パート_シーン_カット_バージョン")
        preview_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        filename_layout.addWidget(preview_label)
        
        filename_group.setLayout(filename_layout)
        main_layout.addWidget(filename_group)
        
        self.setLayout(main_layout)
    
    def update_element_list(self):
        """Update the element list with current order"""
        self.element_list.clear()
        for element in self.filename_config.get_element_order():
            item = QListWidgetItem(self.filename_config.get_element_name(element))
            item.setData(Qt.UserRole, element)
            self.element_list.addItem(item)
    
    def move_element_up(self):
        """Move selected element up in the order"""
        current_row = self.element_list.currentRow()
        if current_row > 0:
            element = self.element_list.currentItem().data(Qt.UserRole)
            if self.filename_config.move_element_up(element):
                self.update_element_list()
                self.element_list.setCurrentRow(current_row - 1)
                self.emit_order_changed()
    
    def move_element_down(self):
        """Move selected element down in the order"""
        current_row = self.element_list.currentRow()
        if current_row < self.element_list.count() - 1 and current_row >= 0:
            element = self.element_list.currentItem().data(Qt.UserRole)
            if self.filename_config.move_element_down(element):
                self.update_element_list()
                self.element_list.setCurrentRow(current_row + 1)
                self.emit_order_changed()
    
    def reset_element_order(self):
        """Reset element order to default"""
        self.filename_config.element_order = self.filename_config.DEFAULT_ORDER.copy()
        self.update_element_list()
        self.emit_order_changed()
    
    def update_prefix(self):
        """Update prefix in the model when input changes"""
        self.filename_config.set_prefix(FilenameConfig.PART, self.part_prefix_input.text())
        self.filename_config.set_prefix(FilenameConfig.SCENE, self.scene_prefix_input.text())
        self.filename_config.set_prefix(FilenameConfig.CUT, self.cut_prefix_input.text())
        self.filename_config.set_prefix(FilenameConfig.VERSION, self.version_prefix_input.text())
        self.emit_prefix_changed()
    
    def reset_prefixes(self):
        """Reset prefixes to default values"""
        self.filename_config.prefixes = self.filename_config.DEFAULT_PREFIXES.copy()
        self.emit_prefix_changed()
    
    def emit_order_changed(self):
        """Emit signal that order has changed"""
        self.filename_order_changed.emit(self.filename_config.get_element_order())
    
    def emit_prefix_changed(self):
        """Emit signal that prefixes have changed"""
        self.prefix_changed.emit(self.filename_config.get_all_prefixes())
    
    def get_filename_order(self):
        """Get current filename element order"""
        return self.filename_config.get_element_order()
    
    def get_prefixes(self):
        """Get current prefixes"""
        return self.filename_config.get_all_prefixes()
    
    def get_ip(self):
        """Get the current IP address from input"""
        return self.ip_input.text()
    
    def get_port(self):
        """Get the current port from input"""
        return self.port_input.value()
    
    def update_prefix_inputs_from_config(self):
        """Update prefix input fields from the filename config"""
        self.part_prefix_input.setText(self.filename_config.get_prefix(FilenameConfig.PART))
        self.scene_prefix_input.setText(self.filename_config.get_prefix(FilenameConfig.SCENE))
        self.cut_prefix_input.setText(self.filename_config.get_prefix(FilenameConfig.CUT))
        self.version_prefix_input.setText(self.filename_config.get_prefix(FilenameConfig.VERSION))
