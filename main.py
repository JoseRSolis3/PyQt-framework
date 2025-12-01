from PyQt6.QtWidgets import QApplication
from log_util import advanced_log, info, warning, error, debug
from dictionaries.builders import App, Logic, Size, Alignment, Layout

app = App("my application")
page = app.page("Login")
loginShell = app.widgetShell("LoginTitle", layout=Layout.vertical)
loginTitle = app.label("LoginTitle", "titleLabel", "Login", 35)
loginTitle2 = app.label("LoginTitle", "title2", "second title", 20)
dropdown1 = app.drop_down("LoginTitle", ("English", "Spanish"), None, "languages")
input1 = app.lineEdit("LoginTitle", "enter text here", "entry1")
button1 = app.button("LoginTitle", "button", None, "button1", dummy=True)
advanced_log(info, f"{app.pageDirectory}")
app.run()