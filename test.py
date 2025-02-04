from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys
from PyQt6.QtCore import QUrl

app = QApplication(sys.argv)
window = QMainWindow()
browser = QWebEngineView()
browser.setUrl(QUrl("https://www.qt.io"))  # or any valid URL
window.setCentralWidget(browser)
window.show()
sys.exit(app.exec())
