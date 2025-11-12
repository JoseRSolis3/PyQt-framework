from log_util import advanced_log
from dictionaries.builders import application, stacked, page, drop_down, widget_shell
from dictionaries.builders import class_name
from PyQt6.QtWidgets import QApplication
import sys

class App():
    def __init__(self):
        self.pages = [Login().parent_w()]
        w = stacked(self.pages[0])
        application(w, "App")
    
    def book(self, pg):
        advanced_log("info",f"Appending {pg} to {self.pages}")
        self.pages.append(pg)
    
    def page_flipper(self, x):
        pass
    
class Login():
    def __init__(self):
        self.children = []
        self.top_menu()

    def parent_w(self):
        return page((500,300), self.children, "login")
    
    def top_menu(self):
        children = []

        mode_items = ["dark", "light", "retro"]
        mode_menu = drop_down(mode_items, None)
        children.append(mode_menu)
        advanced_log("debug",f"Appended {class_name(mode_menu)} to {children}")

        language_items = ["English", "Spanish"]
        language_menu = drop_down(language_items, None)
        children.append(language_menu)
        advanced_log("debug",f"Appended {class_name(language_menu)} to {children}")

        shell = widget_shell("horizontal", children)
        advanced_log("debug",f"Passing Children:{class_name(children)} to Shell: {class_name(shell)}")

        self.children.append(shell)
        return shell

if __name__ == "__main__":
    initialize = QApplication(sys.argv)
    advanced_log("info",f"Iinitializing App")
    app = App()

    page_connector = lambda page: page(app)

    sys.exit(initialize.exec())
