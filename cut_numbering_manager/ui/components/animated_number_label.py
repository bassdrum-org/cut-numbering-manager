"""
アニメーション付き数字ラベル
Animated number label for dial-like animation effects.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint
from PyQt5.QtGui import QPainter, QFont


class AnimatedNumberLabel(QWidget):
    """A label that shows a dial-like animation when the number changes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.old_text = ""
        self.new_text = ""
        self.animation_progress = 0.0
        self.animation = QPropertyAnimation(self, b"animationProgress")
        self.animation.setDuration(500)  # 500ms for animation
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self.font_size = 84
        self.font_weight = "bold"
        self.text_color = "#ffffff"
        
        self.setMinimumHeight(100)
        
    def setText(self, text):
        """Set text with animation"""
        if text == self.new_text:
            return
            
        self.old_text = self.new_text
        self.new_text = text
        
        if self.old_text:
            self.animation_progress = 0.0
            self.animation.setStartValue(0.0)
            self.animation.setEndValue(1.0)
            self.animation.start()
        else:
            self.animation_progress = 1.0
            self.update()
    
    def getText(self):
        """Get current text"""
        return self.new_text
    
    def setFontSize(self, size):
        """Set font size"""
        self.font_size = size
        self.update()
    
    def setFontWeight(self, weight):
        """Set font weight"""
        self.font_weight = weight
        self.update()
    
    def setTextColor(self, color):
        """Set text color"""
        self.text_color = color
        self.update()
    
    def getAnimationProgress(self):
        """Get animation progress"""
        return self.animation_progress
    
    def setAnimationProgress(self, progress):
        """Set animation progress and trigger repaint"""
        self.animation_progress = progress
        self.update()
    
    animationProgress = pyqtProperty(float, getAnimationProgress, setAnimationProgress)
    
    def paintEvent(self, event):
        """Paint the animated text"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        font = QFont()
        font.setFamily("'Inter', 'Noto Sans', 'Arial', 'Helvetica', sans-serif")
        font.setPixelSize(self.font_size)
        if self.font_weight == "bold":
            font.setBold(True)
        painter.setFont(font)
        
        painter.setPen(self.text_color)
        
        rect = self.rect()
        
        if self.animation_progress < 1.0 and self.old_text:
            old_y_offset = -self.animation_progress * rect.height()
            old_rect = rect.translated(0, old_y_offset)
            painter.drawText(old_rect, Qt.AlignRight | Qt.AlignBottom, self.old_text)
            
            new_y_offset = (1.0 - self.animation_progress) * rect.height()
            new_rect = rect.translated(0, new_y_offset)
            painter.drawText(new_rect, Qt.AlignRight | Qt.AlignBottom, self.new_text)
        else:
            painter.drawText(rect, Qt.AlignRight | Qt.AlignBottom, self.new_text)
