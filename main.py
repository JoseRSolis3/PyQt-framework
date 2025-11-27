from PyQt6.QtWidgets import QApplication
from dictionaries.builders import App, Widgets, Logic, universalLibrary, Size, Alignment, Layout

def userDashboard(username: str):
    Widgets.page(username)

def loginPage():
    Widgets.page("login")
    def onLogin():
        print("Login Clicked")
    def onRegister():
        print("Register Clicked")
    Widgets.widget_shell("login", Layout.horizontal, Alignment.default, "title")
    Widgets.label("title", "Login", "Login label", 40)

    Widgets.widget_shell("login", Layout.horizontal, Alignment.default, "username row")
    Widgets.label("username row", "Username:", "username label", None)
    Widgets.entry("username row", "username", "username input")

    Widgets.widget_shell("login", Layout.horizontal, Alignment.default, "password row")
    Widgets.label("password row", "Password:", "password label", None)
    Widgets.entry("password row", "Password", "password input", hidden=True)

    Widgets.widget_shell("login", Layout.horizontal, Alignment.default, "login buttons")
    Widgets.button("login buttons", "Login", onLogin, "login button")
    Widgets.button("login buttons", "Register", onRegister, "register")
App.Initialize("My app")
Widgets.stacked()

loginPage()
Logic.findIndex("login")

Widgets.application(("stack",), "My App")
App.run("My app")
