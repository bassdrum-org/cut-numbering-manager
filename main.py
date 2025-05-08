"""
カット番号管理システム (Cut Numbering Manager)
Entry point for the application.
"""

import sys
import os

os.environ["QT_LOGGING_RULES"] = "qt5ct.debug=false"

from PyQt5.QtWidgets import QApplication
from cut_numbering_manager.ui.main_window import MainWindow


def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
