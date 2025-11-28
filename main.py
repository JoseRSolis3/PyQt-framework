from PyQt6.QtWidgets import QApplication
from dictionaries.builders import App, Widgets, Logic, universalLibrary, Size, Alignment, Layout

def userDashboard(username: str):
    Widgets.page(username)

def registerUser():
    Widgets.page("register")
    def onBack():
        print("Back Pressed")
        Logic.currentIndex("login")
    Widgets.widget_shell("register", Layout.horizontal, Alignment.default, "user title")
    Widgets.label("user title", "User Information", "user information", 30)

    Widgets.widget_shell("register", Layout.horizontal, Alignment.default, "name")
    Widgets.widget_shell("name", Layout.vertical, Alignment.default, "fname")
    Widgets.label("fname", "First Name:", "firstName", None)
    Widgets.entry("fname", "First Name", "firstNameEntry")
    Widgets.widget_shell("name", Layout.vertical, Alignment.default, "lname")
    Widgets.label("lname", "Last Name:", "lastName", None)
    Widgets.entry("lname", "Last Name", "lastNameEntry")

    Widgets.widget_shell("register", Layout.horizontal, Alignment.default, "profile")
    Widgets.widget_shell("profile", Layout.vertical, Alignment.default, "username")
    Widgets.label("username", "Username:", "usernameLabel", None)
    Widgets.entry("username", "username", "usernameEntry")
    Widgets.widget_shell("profile", Layout.vertical, Alignment.default, "email")
    Widgets.label("email", "E-mail:", "emailLable", None)
    Widgets.entry("email", "E-mail", "emailEntry")

    Widgets.widget_shell("register", Layout.horizontal, Alignment.default, "passwordBlock")
    Widgets.widget_shell("passwordBlock", Layout.vertical, Alignment.default, "password")
    Widgets.label("password", "Password:", "passwordLabel", None)
    Widgets.entry("password", "Password", "passwordEntry", hidden = True)
    Widgets.widget_shell("passwordBlock", Layout.vertical, Alignment.default, "reEntry")
    Widgets.label("reEntry", "Re-enter Password:", "reEnterPasswordLable", None)
    Widgets.entry("reEntry", "Password", "reEnterPasswordEntry",hidden = True)

    Widgets.widget_shell("register", Layout.horizontal, Alignment.default, "registerButtons")
    Widgets.button("registerButtons", "Back", onBack, "back")
    Widgets.button("registerButtons", "register", None, "registerButton", dummy = True)



def loginPage():
    Widgets.page("login")
    def onLogin():
        print("Login Clicked")
    def onRegister():
        print("Register Clicked")
        Logic.currentIndex("register")
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
registerUser()
Logic.findIndex("login")

Widgets.application(("stack",), "My App")
App.run("My app")
