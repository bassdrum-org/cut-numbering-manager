"""
メインウィンドウ
Main application window.
"""

import sys
import os
import platform

if platform.system() == "Darwin":  # macOS specific settings
    os.environ["QT_MAC_WANTS_LAYER"] = "1"  # Fix for macOS rendering issues
    if "QT_QPA_PLATFORM" in os.environ:
        del os.environ["QT_QPA_PLATFORM"]  # Avoid offscreen rendering on macOS
elif "DISPLAY" not in os.environ:
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QGroupBox, QTabWidget)
from PyQt5.QtCore import Qt

from cut_numbering_manager.ui.components.cut_info_panel import CutInfoPanel
from cut_numbering_manager.ui.components.settings_panel import SettingsPanel
from cut_numbering_manager.ui.components.preview_panel import PreviewPanel
from cut_numbering_manager.ui.components.clapperboard_panel import ClapperboardPanel
from cut_numbering_manager.models.cut_info import CutInfo
from cut_numbering_manager.utils.filename import generate_filename
from cut_numbering_manager.osc.sender import CustomOSCSender
from cut_numbering_manager.config import (
    APP_NAME, 
    APP_GEOMETRY, 
    OSC_RECORDING_COMMAND,
    OSC_FILENAME_COMMAND
)


class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setGeometry(*APP_GEOMETRY)
        
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Courier New', monospace;
            }
            QGroupBox {
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QTabWidget::pane {
                border: 1px solid #3a3a3a;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #cccccc;
                border: 1px solid #3a3a3a;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 5px 10px;
                min-width: 50px;
            }
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                color: #ffd900;
                border-bottom: none;
            }
            QLineEdit, QSpinBox {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QPushButton:pressed {
                background-color: #4a4a4a;
            }
        """)
        
        self.recording = False
        self.cut_info = CutInfo()
        
        self._init_ui()
        self.update_filename_preview()
    
    def _init_ui(self):
        """Initialize the UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        tabs = QTabWidget()
        main_tab = QWidget()
        settings_tab = QWidget()
        
        tabs.addTab(main_tab, "メイン")
        tabs.addTab(settings_tab, "設定")
        
        main_layout.addWidget(tabs)
        
        main_tab_layout = QVBoxLayout(main_tab)
        
        self.clapperboard_panel = ClapperboardPanel(self.cut_info)
        main_tab_layout.addWidget(self.clapperboard_panel)
        
        self.cut_info_panel = CutInfoPanel(self.cut_info, self.update_ui)
        main_tab_layout.addWidget(self.cut_info_panel)
        
        self.preview_panel = PreviewPanel()
        main_tab_layout.addWidget(self.preview_panel)
        
        rec_group = QGroupBox("録画コントロール")
        rec_layout = QVBoxLayout()
        
        self.rec_button = QPushButton("REC")
        self.rec_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #ff0000;"
            "   color: white;"
            "   font-weight: bold;"
            "   border-radius: 5px;"
            "   min-height: 50px;"
            "   font-size: 16px;"
            "   border: 2px solid #ffffff;"
            "}"
            "QPushButton:pressed {"
            "   background-color: #aa0000;"
            "   border: 2px solid #aaaaaa;"
            "}"
        )
        self.rec_button.clicked.connect(self.toggle_recording)
        
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        rec_layout.addWidget(self.rec_button)
        rec_layout.addWidget(self.status_label)
        
        rec_group.setLayout(rec_layout)
        main_tab_layout.addWidget(rec_group)
        
        settings_tab_layout = QVBoxLayout(settings_tab)
        self.settings_panel = SettingsPanel()
        settings_tab_layout.addWidget(self.settings_panel)
    
    def update_filename_preview(self):
        """Update the filename preview based on current inputs"""
        filename = generate_filename(self.cut_info)
        self.preview_panel.update_preview(filename)
    
    def update_ui(self):
        """Update all UI components from the model"""
        self.update_filename_preview()
        self.clapperboard_panel.update_ui_from_model()
    
    def toggle_recording(self):
        """Toggle recording state and send appropriate OSC message"""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording and send OSC message"""
        try:
            ip = self.settings_panel.get_ip()
            port = self.settings_panel.get_port()
            
            filename = generate_filename(self.cut_info)
            print(f"録画ファイル名を設定: {filename}")
            
            sender = CustomOSCSender(ip, port)
            filename_success = sender.send_message_standard(OSC_FILENAME_COMMAND, filename)
            
            if not filename_success:
                print("ファイル名設定コマンドの送信に失敗しました。録画は続行します。")
            
            success = sender.send_message_standard(OSC_RECORDING_COMMAND, 1)
            
            if success:
                self.recording = True
                self.rec_button.setText("STOP")
                self.status_label.setText(f"録画中: {filename}")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.status_label.setText("OSCメッセージの送信に失敗しました")
                self.status_label.setStyleSheet("color: red;")
            
        except Exception as e:
            self.status_label.setText(f"エラー: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
    
    def stop_recording(self):
        """Stop recording, send OSC message, and update cut/version numbers"""
        try:
            ip = self.settings_panel.get_ip()
            port = self.settings_panel.get_port()
            
            sender = CustomOSCSender(ip, port)
            success = sender.send_message_standard(OSC_RECORDING_COMMAND, 0)
            
            if success:
                self.recording = False
                self.rec_button.setText("REC")
                
                self.cut_info.increment_cut()
                self.cut_info_panel.update_ui_from_model()
                self.clapperboard_panel.update_ui_from_model()
                
                self.update_filename_preview()
                
                next_filename = generate_filename(self.cut_info)
                print(f"次の録画用ファイル名を設定: {next_filename}")
                
                self.status_label.setText(f"録画完了: {next_filename}")
                self.status_label.setStyleSheet("color: blue;")
            else:
                self.status_label.setText("OSCメッセージの送信に失敗しました")
                self.status_label.setStyleSheet("color: red;")
            
        except Exception as e:
            self.status_label.setText(f"エラー: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
