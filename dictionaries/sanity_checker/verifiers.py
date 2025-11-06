from PyQt6.QtWidgets import (
    QApplication,QMainWindow, QWidget, QStackedWidget, 
    QPushButton, QLabel, QLineEdit, QComboBox, 
    QVBoxLayout, QHBoxLayout, QFormLayout,
)
from PyQt6.QtCore import Qt
from variable_cleaner import cleaner
from log_util import advanced_log
from functools import reduce
import inspect
import sys 
import os

advanced_log("info", "Cleaning done, continuing with verification.")
class_name = lambda var: var.__class__.__name__
reminder = "|**REMINDER**|"

# (var, attr, value) -> executes var.attr(value)
command = lambda var, a, v: getattr(var, a)(v)

# (var, nested_attr_path, value) -> executes var.attr1().attr2(...)(value)
command_nested = lambda var, path, v: reduce(getattr,path.split('.'), var)(v)

widgets_list = {
    "application":QApplication,
    "main window":QMainWindow,
    "widget":QWidget,
    "stacked":QStackedWidget,
    "button":QPushButton,
    "label":QLabel,
    "input":QLineEdit,
    "drop down":QComboBox
}

layouts_list = {
    "vertical":QVBoxLayout,
    "horizontal":QHBoxLayout,
    "form":QFormLayout}

widget_attributes = {
    QMainWindow : ["setCentralWidget", "show"],
    QWidget : ["setLayout"],
    QLabel : [("setText", str)],
    QComboBox : [("addItem", str), ("addItems", list)],
    QLineEdit : [("setPlaceholderText", str)]
}

class verifier():
    def __init__(self, widget, layout):
        self.instantiated_variables = []
        self.widget_verifier(widget)
        self.layout_verifier(layout)

    def widget_verifier(self, widget):
        advanced_log("info","Initiating widget verification.")
        # Run the cleaner
        cleaned_widget = cleaner(widget)

        # Check if the widget exists
        if cleaned_widget in widgets_list:
            advanced_log("info","Entered text matched token.")
            # Convert the cleaned_widget text to its instance
            cls = widgets_list[cleaned_widget]
            # Check if the class matches the widget
            if cls is QApplication:
                # Append (sys.argv) to QApplication
                instance = cls(sys.argv)
                advanced_log("info","QApplication detected. Auto appended sys.argv as the argument")
                self.instantiated_variables.append(instance)
            else:
                instance = cls()
                self.instantiated_variables.append(instance)
        else:
            advanced_log("warning","Entered text did not match a token. Please try again.")
            return None

    def layout_verifier(self, layout):
        advanced_log("info", "Initiating layout verifier.")
        cleaned_layout = cleaner(layout)
        if cleaned_layout in layouts_list:
            cls = layouts_list[cleaned_layout]
            instance = cls()
            self.instantiated_variables.append(instance)
        else:
            advanced_log("warning", "Layout does not exist in list. Please try again.")
            return None
        
    # TODO Size Verifier
    def size_verifier(self, size):
        advanced_log("info", "Initiating size verifier.")
        # TODO cleaner
        cleaned_size = cleaner(size)
        # Check if size is a list
        if isinstance(cleaned_size, (list, tuple)):
            # Create a list with the verified numbers
            verified_size = []
            # Iterate through the list/tuple
            for n in cleaned_size:
                if isinstance(n, (int, float)):
                    # Add the verified number into the list
                    verified_size.append(n)
            # Check the length of the list
            if len(verified_size) == 2:
                advanced_log("info", "Resize detected")
                # Find widget in the the instantiated variables list
                for var in self.instantiated_variables:
                    # Check each item to see if it has the resize attribute
                    if hasattr(var, "resize"):
                        var.resize(*verified_size)
                    else:
                        advanced_log("critical", "Widget does not possess the 'resize' attribute.")
            elif len(verified_size) == 4:
                advanced_log("info", "Geometry detected.")
                for var in self.instantiated_variables:
                    if hasattr(var, "setGeometry"):
                        var.setGeometry(*verified_size)
                    else:
                        advanced_log("critical", "Widget does not possess the 'setGeometry' attribute.")
            else:
                advanced_log("warning", "List/tuple length is invalid. Please try again.")
        else:
            advanced_log("warning", "Entered data type is not list/tuple. Please try again")

    # TODO Alignment Verifier
        # TODO cleaner
        # TODO list check
            # TODO instantiate
        # TODO else 

    # TODO Child Verifier
        # TODO cleaner
        # TODO list check
            # TODO instantiate
        # TODO else 

    # TODO Style Verifier
        # TODO cleaner
        # TODO list check
            # TODO instantiate
        # TODO else 

    # TODO Object Name Verifier
        # TODO cleaner
        # TODO list check
            # TODO instantiate
        # TODO else 
