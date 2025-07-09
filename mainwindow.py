# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow ,QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtCore import QUrl

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.browser = QWebEngineView(self)
        self.profile = QWebEngineProfile.defaultProfile()
        layout = QVBoxLayout(self.ui.page_1)
        layout.addWidget(self.browser)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        self.browser.urlChanged.connect(self.on_url_changed)
        self.browser.setUrl(QUrl("https://ft-eu.gehealthcare.com/EFTClient/Account/Login.htm"))

    def on_url_changed(self, url):
        print(f"Page navigated to: {url.toString()}")
        if "/Home" in url.toString():
            print("Logged in! Capturing cookies...")
            self.dump_cookies()

    def dump_cookies(self):
        cookie_store = self.profile.cookieStore()
        cookie_store.cookiesAdded.connect(self.save_cookies)
        cookie_store.loadAllCookies()

    def save_cookies(self, cookies):
        cookies_saved = False
        for cookie in cookies:
            name = bytes(cookie.name()).decode()
            value = bytes(cookie.value()).decode()
            domain = cookie.domain()
            path = cookie.path()
            print(f"Cookie: {name}={value}; Domain={domain}; Path={path}")
            with open("cookies.txt", "a") as f:
                f.write(f"{name}={value}; domain={domain}; path={path}\n")
            cookies_saved = True
        if cookies_saved:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        else:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
