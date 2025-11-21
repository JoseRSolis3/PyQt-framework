from log_util import advanced_log
from dictionaries.builders import Widgets, class_name, Size, Alignment, Layout
from PyQt6.QtWidgets import QApplication
import sys

class App():
    def __init__(self):
        self.pages = [Login().parentWidget()]
        w = Widgets.stacked(self.pages[0])
        w.setCurrentIndex(0)
        Widgets.application(w, "App")
    
    def book(self, pg):
        advanced_log("info",f"Appending {pg} to {self.pages}")
        self.pages.append(pg)
    
    def page_flipper(self, x):
        pass
    
class Login():
    def __init__(self):
        self.children = []
        self.top_menu()
        self.username()
        self.password()
        self.Buttons()

    def parentWidget(self):
        return Widgets.page((500,300), self.children, "login")
    
    def top_menu(self):
        children = []

        mode_items = ["dark", "light", "retro"]
        mode_menu = Widgets.drop_down(mode_items, None, (Size.max, Size.default))
        children.append(mode_menu)
        advanced_log("debug",f"Appended {class_name(mode_menu)} to {children}")

        language_items = ["English", "Spanish"]
        language_menu = Widgets.drop_down(language_items, None, (Size.max, Size.default))
        children.append(language_menu)
        advanced_log("debug",f"shell = Widgets.widget_shell(Layout.horizontal -> {class_name(Layout.horizontal)}, Alignment.top_right -> {class_name(Alignment.top_right)}, childrent -> {children})")
        shell = Widgets.widget_shell(Layout.horizontal, Alignment.top_right, children)
        advanced_log("debug",f" SHELL AFTER INSTANTIATION = {shell}")

        self.children.append(shell)
        return shell
        
    def username(self):
        child = []

        username = Widgets.label("Username:")
        child.append(username)
        userentry = Widgets.entry("username")
        child.append(userentry)

        shell = Widgets.widget_shell(Layout.horizontal,None, child)

        self.children.append(shell)
        return shell
    
    def password(self):
        child = []
        pw = Widgets.label("Password:")
        child.append(pw)
        userentry = Widgets.entry("password")
        child.append(userentry)
        shell = Widgets.widget_shell(Layout.horizontal, Alignment.default, child)
        self.children.append(shell)
        return shell
    
    def Buttons(self):
        children = []
        signinButton = Widgets.button("signin", None)
        children.append(signinButton)
        signupButton = Widgets.button("signup", None)
        children.append(signupButton)
        shell = Widgets.widget_shell(Layout.horizontal, Alignment.default, children)
        self.children.append(shell)
        return shell

class userDashboard():
    pass 
if __name__ == "__main__":
    initialize = QApplication(sys.argv)
    advanced_log("info",f"Iinitializing App")
    app = App()

    page_connector = lambda page: page(app)

    sys.exit(initialize.exec())
