"""
OSC送信モジュール
OSC message sending functionality for OBS communication.
"""

import socket
from pythonosc import udp_client


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
