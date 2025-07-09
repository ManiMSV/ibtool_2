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
        self.ui.page_1.setLayout(layout)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)
        self.browser.setUrl(QUrl("https://ft-eu.gehealthcare.com/EFTClient/Account/Login.htm"))
        self.browser.urlChanged.connect(self.on_url_changed)

    def on_url_changed(self, url):
        url_str = url.toString()
        print(f"Page navigated to: {url_str}")
        if "/Home" in url_str:
            print("Logged in! Attempting to collect CSRF token...")
            self.collect_csrf_token()

    def collect_csrf_token(self):
        # Run JavaScript to get CSRF token from cookies
        js = """
            (function() {
                let csrf = "";
                document.cookie.split(';').forEach(function(cookie) {
                    let [name, value] = cookie.split('=');
                    if (name && name.trim().toLowerCase().includes('csrf')) {
                        csrf = value;
                    }
                });
                return csrf;
            })();
        """
        self.browser.page().runJavaScript(js, self.handle_csrf_token)

    def handle_csrf_token(self, token):
        print(f"CSRF Token: {token}")
        # You can store the token or use it as needed here
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

    def setup_page_2(self):
        self.ui.pushButton_go.clicked.connect(self.on_go_clicked)

    def on_go_clicked(self):
        url = self.ui.lineEdit_pastelink.text().strip()
        if not url:
            print("No URL entered.")
            return
        # Use the previously collected CSRF token if needed
        # For demonstration, we'll just print it and load the URL
        print(f"Loading URL: {url} with CSRF Token: {getattr(self, 'csrf_token', None)}")
        self.browser.setUrl(QUrl(url))

    def handle_csrf_token(self, token):
        print(f"CSRF Token: {token}")
        self.csrf_token = token
        self.setup_page_2()
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)


    # def on_url_changed(self, url):
    #     print(f"Page navigated to: {url.toString()}")
    #     if "/Home" in url.toString():
    #         print("Logged in! Capturing cookies...")
    #         self.dump_cookies()

    # def dump_cookies(self):
    #     cookie_store = self.profile.cookieStore()
    #     cookie_store.cookiesAdded.connect(self.save_cookies)
    #     cookie_store.loadAllCookies()

    # def save_cookies(self, cookies):
    #     cookies_saved = False
    #     for cookie in cookies:
    #         name = bytes(cookie.name()).decode()
    #         value = bytes(cookie.value()).decode()
    #         domain = cookie.domain()
    #         path = cookie.path()
    #         print(f"Cookie: {name}={value}; Domain={domain}; Path={path}")
    #         with open("cookies.txt", "a") as f:
    #             f.write(f"{name}={value}; domain={domain}; path={path}\n")
    #         cookies_saved = True
    #     if cookies_saved:
    #         self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
    #     else:
    #         pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
