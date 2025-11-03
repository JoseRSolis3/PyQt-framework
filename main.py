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
        self.children = []
        self.mw = self.main_window()
        sys.exit(self.app.exec())

    @safestart
    def main_window(self):
        central_widget = widgetFactory().widget_without_text_builder("widget", "vertical", "vertical", None, None, self.children, "central widget")
        main_window = widgetFactory().widget_without_text_builder("main window", None, None, "App", (100,100,500,300), central_widget, "main window")
        return main_window
    

class loginPage():
    def __init__(self):
        self.login_children = []
        self.titleRow()
        self.pageWidget()

    @safestart
    def titleRow(self):
        titleWidget = widgetFactory().widget_with_text_builder("label", "Title", "center", None, None, "title row")
        self.login_children.append(titleWidget)
        return titleWidget   
     
    @safestart
    def pageWidget(self):
        page = widgetFactory().widget_without_text_builder("widget", "vertical", None, None, None, self.login_children, "login page")
        log.debug(f"{class_name(page)}")
        return page
    


if __name__ == "__main__":
    app = App()