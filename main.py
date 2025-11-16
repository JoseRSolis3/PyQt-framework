from log_util import advanced_log
from dictionaries.builders import Widgets, class_name, Size, Alignment
from PyQt6.QtWidgets import QApplication
import sys

class App():
    def __init__(self):
        self.pages = [Login().parent_w()]
        w = Widgets.stacked(self.pages[0])
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
        self.title()
        self.username()
        self.password()

    def parent_w(self):
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
        advanced_log("debug",f"Appended {class_name(language_menu)} to {children}")

        shell = Widgets.widget_shell(Alignment.top_right, "horizontal", children)
        advanced_log("debug",f"Passing Children:{class_name(children)} to Shell: {class_name(shell)}")

        self.children.append(shell)
        return shell
    
    def title(self):
        child = []
        title = Widgets.label("Login")
        child.append(title)
        shell = Widgets.widget_shell(None, "horizontal", child)

        self.children.append(shell)
        return shell       
    
    def username(self):
        child = []

        username = Widgets.label("Username:")
        child.append(username)
        userentry = Widgets.entry("username")
        child.append(userentry)

        shell = Widgets.widget_shell(None, "horizontal", child)

        self.children.append(shell)
        return shell
    
    def password(self):
        child = []
        pw = Widgets.label("Password:")
        child.append(pw)
        userentry = Widgets.entry("password")
        child.append(userentry)
        shell = Widgets.widget_shell(None, "horizontal", child)
        self.children.append(shell)
        return shell


if __name__ == "__main__":
    initialize = QApplication(sys.argv)
    advanced_log("info",f"Iinitializing App")
    app = App()

    page_connector = lambda page: page(app)

    sys.exit(initialize.exec())
