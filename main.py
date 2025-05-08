"""
カット番号管理システム (Cut Numbering Manager)
This application provides a GUI for managing cut numbers in anime production,
with OSC integration for OBS recording control.
"""

import sys
import os
import re
import platform
import socket

if platform.system() == "Darwin":  # macOS specific settings
    os.environ["QT_MAC_WANTS_LAYER"] = "1"  # Fix for macOS rendering issues
    if "QT_QPA_PLATFORM" in os.environ:
        del os.environ["QT_QPA_PLATFORM"]  # Avoid offscreen rendering on macOS
elif "DISPLAY" not in os.environ:
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                            QLineEdit, QFormLayout, QGroupBox, QSpinBox,
                            QTabWidget, QSplitter, QComboBox)
from PyQt5.QtCore import Qt
from pythonosc import udp_client

os.environ["QT_LOGGING_RULES"] = "qt5ct.debug=false"

class CustomOSCSender:
    """Custom OSC message sender with multiple formatting options for compatibility"""
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send_message_with_space(self, address, value):
        """Send an OSC message with a space between address and value"""
        message = f"{address} {value}"
        print(f"送信 (スペース区切り): {message}")
        try:
            self.socket.sendto(message.encode(), (self.ip, self.port))
            return True
        except Exception as e:
            print(f"エラー: {str(e)}")
            return False
    
    def send_message_with_comma(self, address, value):
        """Send an OSC message with a comma between address and value"""
        message = f"{address},{value}"
        print(f"送信 (カンマ区切り): {message}")
        try:
            self.socket.sendto(message.encode(), (self.ip, self.port))
            return True
        except Exception as e:
            print(f"エラー: {str(e)}")
            return False
    
    def send_message_standard(self, address, value):
        """Send an OSC message using the standard python-osc library"""
        client = udp_client.SimpleUDPClient(self.ip, self.port)
        print(f"送信 (標準OSC形式): {address} {value}")
        try:
            client.send_message(address, value)
            return True
        except Exception as e:
            print(f"エラー: {str(e)}")
            return False
            
    def send_message_raw(self, address, value=None):
        """Send an OSC message as a raw string without any formatting"""
        message = address if value is None else f"{address}{value}"
        print(f"送信 (生データ): {message}")
        try:
            self.socket.sendto(message.encode(), (self.ip, self.port))
            return True
        except Exception as e:
            print(f"エラー: {str(e)}")
            return False

class CutNumberingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("カット番号管理システム")
        self.setGeometry(300, 300, 600, 500)
        
        self.recording = False
        self.current_cut_number = 1
        self.current_version = 1
        
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
        
        cut_info_group = QGroupBox("カット情報")
        cut_info_layout = QFormLayout()
        
        self.part_input = QLineEdit("Part1")
        cut_info_layout.addRow("パート名:", self.part_input)
        self.part_input.textChanged.connect(self.update_filename_preview)
        
        self.scene_input = QLineEdit("Scene1")
        cut_info_layout.addRow("シーン名:", self.scene_input)
        self.scene_input.textChanged.connect(self.update_filename_preview)
        
        self.cut_number_input = QSpinBox()
        self.cut_number_input.setRange(1, 9999)
        self.cut_number_input.setValue(self.current_cut_number)
        cut_info_layout.addRow("カット番号:", self.cut_number_input)
        self.cut_number_input.valueChanged.connect(self.update_filename_preview)
        
        self.version_input = QSpinBox()
        self.version_input.setRange(1, 999)
        self.version_input.setValue(self.current_version)
        cut_info_layout.addRow("バージョン:", self.version_input)
        self.version_input.valueChanged.connect(self.update_filename_preview)
        
        cut_info_group.setLayout(cut_info_layout)
        main_tab_layout.addWidget(cut_info_group)
        
        preview_group = QGroupBox("ファイル名プレビュー")
        preview_layout = QVBoxLayout()
        
        self.filename_preview = QLabel()
        self.filename_preview.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.filename_preview.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.filename_preview)
        
        preview_group.setLayout(preview_layout)
        main_tab_layout.addWidget(preview_group)
        
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
            "}"
            "QPushButton:pressed {"
            "   background-color: #aa0000;"
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
        
        osc_settings_group = QGroupBox("OSC設定")
        osc_settings_layout = QFormLayout()
        
        self.ip_input = QLineEdit("127.0.0.1")
        osc_settings_layout.addRow("IPアドレス:", self.ip_input)
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(3333)
        osc_settings_layout.addRow("ポート:", self.port_input)
        
        version_note = QLabel("OSC for OBS v2.7.1 (OBS v27.2.4用)")
        version_note.setStyleSheet("font-weight: bold;")
        osc_settings_layout.addRow("バージョン:", version_note)
        
        command_note = QLabel("録画コマンド: /setRecording 1 (開始) / /setRecording 0 (停止)")
        command_note.setStyleSheet("color: #555; font-style: italic;")
        osc_settings_layout.addRow("", command_note)
        
        filename_note = QLabel("ファイル名設定コマンド: /recFileName [filename]")
        filename_note.setStyleSheet("color: #555; font-style: italic;")
        osc_settings_layout.addRow("", filename_note)
        
        osc_settings_group.setLayout(osc_settings_layout)
        settings_tab_layout.addWidget(osc_settings_group)
        
        self.update_filename_preview()
        
    
    def update_filename_preview(self):
        """Update the filename preview based on current inputs"""
        part = self.sanitize_filename(self.part_input.text())
        scene = self.sanitize_filename(self.scene_input.text())
        cut = str(self.cut_number_input.value()).zfill(3)
        version = f"v{str(self.version_input.value()).zfill(2)}"
        
        filename = f"{part}_{scene}_{cut}_{version}"
        self.filename_preview.setText(filename)
    
    def sanitize_filename(self, name):
        """Remove invalid characters from filename"""
        return re.sub(r'[\\/*?:"<>|]', "_", name)
    
    def toggle_recording(self):
        """Toggle recording state and send appropriate OSC message"""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording and send OSC message"""
        try:
            ip = self.ip_input.text()
            port = self.port_input.value()
            
            filename = self.filename_preview.text()
            print(f"録画ファイル名を設定: {filename}")
            
            sender = CustomOSCSender(ip, port)
            filename_success = sender.send_message_with_space("/recFileName", filename)
            
            if not filename_success:
                print("ファイル名設定コマンドの送信に失敗しました。録画は続行します。")
            
            success = sender.send_message_with_space("/setRecording", "1")
            
            if success:
                self.recording = True
                self.rec_button.setText("STOP")
                self.status_label.setText(f"録画中: {self.filename_preview.text()}")
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
            ip = self.ip_input.text()
            port = self.port_input.value()
            
            sender = CustomOSCSender(ip, port)
            success = sender.send_message_with_space("/setRecording", "0")
            
            if success:
                self.recording = False
                self.rec_button.setText("REC")
                
                self.current_cut_number += 1
                self.cut_number_input.setValue(self.current_cut_number)
                
                self.current_version = 1
                self.version_input.setValue(self.current_version)
                
                self.update_filename_preview()
                
                next_filename = self.filename_preview.text()
                print(f"次の録画用ファイル名を設定: {next_filename}")
                
                self.status_label.setText(f"録画完了: {self.filename_preview.text()}")
                self.status_label.setStyleSheet("color: blue;")
            else:
                self.status_label.setText("OSCメッセージの送信に失敗しました")
                self.status_label.setStyleSheet("color: red;")
            
        except Exception as e:
            self.status_label.setText(f"エラー: {str(e)}")
            self.status_label.setStyleSheet("color: red;")

def main():
    app = QApplication(sys.argv)
    window = CutNumberingApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
