from PyQt6.QtWidgets import (
    QApplication,QMainWindow, QWidget,
    QPushButton, QLabel, QLineEdit, QComboBox,
    QVBoxLayout, QHBoxLayout, QFormLayout
)

from PyQt6.QtCore import Qt

from log_util import log
from factories.widget_factory import widgetFactory

import sys
import os

class_name = lambda w: w.__class__.__name__

def safestart(func):
    """Decorator to safely start a function and log any exceptions."""
    def wrapper(*args, **kwargs):
        try:
            print("\n")
            log.debug(f"Starting function: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            log.error(f"Error in ({func.__name__}): {e}")
            return None
    return wrapper

class App():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.mw = self.main_window()
        if hasattr(self.mw, "show"):
            log.debug(f"|INIT VERIFICATION|: self.mw is {class_name(self.mw)} and does have 'show' attribute.")
        else:
            log.error(f"|INIT VERIFICATION|: self.mw is {class_name(self.mw)} and does not have 'show' sttribute")
        self.mw.show()
        sys.exit(self.app.exec())

    @safestart
    def main_window(self):
        self.central_widget = widgetFactory().widget_without_text_builder("widget","vertical", None, None, None, "Central Widget", None) 
        log.debug(f"Entered Central Widget: {class_name(self.central_widget)}")    
        self.mw = widgetFactory().widget_without_text_builder("main window", None, None, (100,100,500,300), "App", self.central_widget, "Main Window")
        log.debug(f"|MAIN WINDOW METHOD VERIFICATION|: Entered Main Window: {class_name(self.mw)}")
        return self.mw
    
    @safestart
    def children(self):
        self.child = [LoginPage().page_constrictor()]
        return self.child

class LoginPage():
    def __init__(self):
        self.login_page_children = []
        log.info(f"Children: {self.login_page_children}")
        self.top_menu()
        self.page_constrictor()
    
    def page_constrictor(self):
        log.info(f"Encapsulating every widget into one page")
        self.page = widgetFactory().widget_without_text_builder("widget", "vertical", "center", None, None, self.login_page_children, "Login Page Constrictor")
        return self.page
    
    @safestart
    def top_menu(self):
        self.menu_items = []

        self.modes = ["Light", "Dark"]
        self.modes_menu = widgetFactory().widget_with_text_builder("drop down", None, "right", None,"mode menu", self.modes)
        self.menu_items.append(self.modes_menu)

        self.languages = ["English", "Spanish"]
        self.language_menu = widgetFactory().widget_with_text_builder("drop down", None, "right", None, None, self.languages, "language menu")
        self.menu_items.append(self.language_menu)

        self.top_menu_constrictor = widgetFactory().widget_without_text_builder("widget", "horizontal", "right", None, None, self.menu_items, "Top Menu Constrictor")

        log.info(f"Menu Items = {self.menu_items} | Constrictor: {self.top_menu_constrictor}")
        self.login_page_children.append(self.top_menu_constrictor)

if __name__ == "__main__":
    app = App()