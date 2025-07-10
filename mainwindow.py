# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtCore import QUrl

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
# from PySide6.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

        # Setup browser
        self.browser = QWebEngineView()
        self.profile = QWebEngineProfile.defaultProfile()
        layout = self.ui.page_2.layout()
        layout.addWidget(self.browser)

        # Connect button
        self.ui.pushButton_go.clicked.connect(self.display_link)

        self.session_id = None

        # Connect cookie handler once
        cookie_store = self.profile.cookieStore()
        cookie_store.cookieAdded.connect(self.handle_cookie)

        # Debug: watch browser events
        self.print_browser_events()

    def display_link(self):
        url_text = self.ui.lineEdit_pastelink.text().strip()
        if not url_text:
            print("No URL entered.")
            return
        if not url_text.startswith("http"):
            url_text = "https://" + url_text
        self.browser.setUrl(QUrl(url_text))

    def handle_cookie(self, cookie):
        name = cookie.name().data().decode()
        value = cookie.value().data().decode()
        print(f"Cookie added: {name} = {value}")

        if name == "websessionid":
            self.session_id = value
            print(f"Session ID fetched: {self.session_id}")

            # Now reload immediately
            self.reload_page_with_session()

    def reload_page_with_session(self):
        url_text = self.ui.lineEdit_pastelink.text().strip()
        if not url_text:
            print("No URL entered for reload.")
            return
        if not url_text.startswith("http"):
            url_text = "https://" + url_text

        print(f"Reloading URL with session ID: {self.session_id}")
        self.browser.setUrl(QUrl(url_text))

    def print_browser_events(self):
        # Useful for debugging page loads
        self.browser.urlChanged.connect(lambda url: print(f"URL changed: {url.toString()}"))
        self.browser.loadStarted.connect(lambda: print("Load started"))
        self.browser.loadProgress.connect(lambda progress: print(f"Load progress: {progress}%"))
        self.browser.loadFinished.connect(lambda ok: print(f"Load finished: {'Success' if ok else 'Failed'}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
