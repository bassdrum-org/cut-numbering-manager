"""
OSC Sender Application with PyQt5 GUI
This application provides a simple GUI with a REC button that sends OSC messages
to a specified IP address and port when clicked.
"""

import sys
import os
if "DISPLAY" not in os.environ:
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                            QLineEdit, QFormLayout, QGroupBox, QSpinBox)
from PyQt5.QtCore import Qt
from pythonosc import udp_client

class OSCSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OSC Sender")
        self.setGeometry(300, 300, 400, 250)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        settings_group = QGroupBox("OSC Settings")
        settings_layout = QFormLayout()
        
        self.ip_input = QLineEdit("127.0.0.1")
        settings_layout.addRow("IP Address:", self.ip_input)
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(8000)
        settings_layout.addRow("Port:", self.port_input)
        
        self.message_input = QLineEdit("/record")
        settings_layout.addRow("OSC Message:", self.message_input)
        
        self.value_input = QLineEdit("1")
        settings_layout.addRow("Value:", self.value_input)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
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
        self.rec_button.clicked.connect(self.send_osc_message)
        
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.rec_button)
        button_layout.addWidget(self.status_label)
        main_layout.addLayout(button_layout)
        
    def send_osc_message(self):
        """Send OSC message when REC button is clicked"""
        try:
            ip = self.ip_input.text()
            port = self.port_input.value()
            message = self.message_input.text()
            value = self.value_input.text()
            
            client = udp_client.SimpleUDPClient(ip, port)
            
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
            
            client.send_message(message, value)
            
            self.status_label.setText(f"Sent {message} {value} to {ip}:{port}")
            self.status_label.setStyleSheet("color: green;")
            
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.status_label.setStyleSheet("color: red;")

def main():
    app = QApplication(sys.argv)
    window = OSCSenderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
