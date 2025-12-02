from PyQt6.QtWidgets import QApplication
from log_util import advanced_log, info, warning, error, debug
from dictionaries.builders import App, Logic, Size, Alignment, Layout

app = App("my application")
class LoginPage():
    def __init__(self) -> None: 
        self.page = app.page("Login", (500,300), fixedSize=True)
        self.topMenu()
        self.title()
        self.form()
    def topMenu(self):
        topMenu = "topMenu"
        self.menuBar = app.widgetShell(topMenu, layout=Layout.horizontal, alignment=Alignment.top_right)
        self.dropdown1 = app.drop_down(topMenu, ("English", "Spanish"), None, "languages")
        self.styles = app.drop_down(topMenu, ("Dark", "Light"), None, "modes")
    def title(self):
        loginTitle = "LoginTitle"
        self.loginTitleShell = app.widgetShell(loginTitle, layout=Layout.horizontal, alignment=Alignment.center)
        loginTitle = app.label(loginTitle, "titleLabel", "Login", 35)
    def form(self):
        loginForm = "LoginForm"
        self.loginFormShell = app.widgetShell(loginForm, layout=Layout.form, alignment=Alignment.center)
        self.input1 = app.lineEdit(loginForm, "enter text here", "entry1")
        self.button1 = app.button(loginForm, "button", None, "button1", dummy=True)
LoginPage()
advanced_log(info, f"{app.pageDirectory}")
app.run()