from PyQt6.QtWidgets import (
    QApplication,QMainWindow, QWidget, QStackedWidget, 
    QPushButton, QLabel, QLineEdit, QComboBox, 
    QVBoxLayout, QHBoxLayout, QFormLayout,
)
from PyQt6.QtCore import Qt
from variable_cleaner import cleaner
from log_util import advanced_log
import inspect
import sys 
import os

advanced_log("info", "Cleaning done, continuing with verification.")
class_name = lambda var: var.__class__.__name__
reminder = "|**REMINDER**|"

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
    "QPushButton": ["text", "enabled", "visible"],
    "QLabel": ["text", "alignment", "visible"],
    "QLineEdit": ["text", "placeholderText", "readOnly"],
    "QComboBox": ["items", "currentIndex", "editable"]
}

def widget_verifier(widget = None):
    advanced_log("info", f"Widget entry is {widget}. Starting widget verification.")

    #cleans the key variable
    cleaned_widget = cleaner(widget)
    advanced_log("info", f"Cleaned widget type is {class_name(cleaned_widget)}.")

    #varifies if the widget is in the widget dictionary
    if isinstance(cleaned_widget, tuple(widgets_list.values())):
        instance = cleaned_widget
        widget_name = class_name(instance)

    #if user passes a string key -> convert it to class
    elif isinstance(cleaned_widget, str): 
        #lookup the widget class from the dictionary
        widget_class = widgets_list.get(cleaned_widget)

        if widget_class is None:
            advanced_log("info", f"Widget class not found for key '{cleaned_widget}'")
            return None
        
        advanced_log("info", f"Widget class found for key '{cleaned_widget}'")
        #Create an instance of the widget | key -> class -> instance | str -> class -> widget
        instance = widget_class()
        widget_name = class_name(instance)
    else:
        advanced_log("warning", f"Invalid widget type: {class_name(cleaned_widget)}. Expected str or Widget instance")
        return None
    
    #Attribute verification
    if widget_name in widget_attributes:
        advanced_log("info", f"Verifying attributes for widget: {widget_name}")

        for attr in widget_attributes[widget_name]:
            if not hasattr(instance, attr):
                advanced_log("warning", f"Widget '{widget_name}' is missing. Expected attribute: '{attr}'.")
            else:
                advanced_log("info", f"Widget '{widget_name}' has expected attribute: '{attr}'.")
    else:
        advanced_log("info", f"No attribute verication list for widget: {widget_name}")

    advanced_log("info", f"Widget verification completed for: {widget_name}")
    return instance
