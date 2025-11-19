from PyQt6.QtWidgets import (
    QApplication,QMainWindow, QWidget, QStackedWidget, 
    QPushButton, QLabel, QLineEdit, QComboBox, 
    QVBoxLayout, QHBoxLayout, QFormLayout,QLayout
)
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import Qt, QMargins
from log_util import advanced_log
from functools import reduce
import inspect
import sys 
import os

class Size():
    auto = QSizePolicy.Policy.Preferred
    fill = QSizePolicy.Policy.Expanding
    fixed = QSizePolicy.Policy.Fixed
    min = QSizePolicy.Policy.Minimum
    max = QSizePolicy.Policy.Maximum
    stretch = QSizePolicy.Policy.Expanding
    default = QSizePolicy.Policy.Expanding

    @staticmethod
    def set(widget, sizeStyle):
        if sizeStyle is None:
            advanced_log("warning",f"Size type is None. Returning default.")
            return Size.default
        elif not isinstance(sizeStyle, (tuple, list)):
            advanced_log("warning",f"Invalid data type. Returning default.")
            return widget.setSizePolicy(Size.default, Size.default)
        else:
            items = list(sizeStyle)
            for i, style in enumerate(sizeStyle):
                if not isinstance(style, QSizePolicy):
                    advanced_log("warning",f"Invalid data type. Returning default.")
                    items[i] = Size.default
                else:
                    items[i] = style
            return widget.setSizePolicy(*items)
                

class Alignment():
    top = Qt.AlignmentFlag.AlignTop
    bottom = Qt.AlignmentFlag.AlignBottom
    left = Qt.AlignmentFlag.AlignLeft
    center = Qt.AlignmentFlag.AlignCenter
    default = Qt.AlignmentFlag.AlignCenter
    hcenter = Qt.AlignmentFlag.AlignHCenter
    vcenter = Qt.AlignmentFlag.AlignVCenter
    right = Qt.AlignmentFlag.AlignRight

    top_left = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
    top_right = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
    bottom_left = Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
    bottom_right = Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight

    @staticmethod
    def set(widget, alignmentFlag):
        return widget.setAlignment(alignmentFlag)


class LayoutType():
    vertical = QVBoxLayout
    horizontal = QHBoxLayout
    form = QFormLayout

widgets = [
    QWidget, QStackedWidget, QPushButton, 
    QLabel, QLineEdit, QComboBox
]

layouts = {
    "vertical" : QVBoxLayout,
    "horizontal" : QHBoxLayout,
    "form" : QFormLayout
}

cleaner = lambda var: var.strip()
class_name = lambda var: var.__class__.__name__
layout_setter = lambda w, l: w.setLayout(l)
    
class Margins():
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def validator(func):
        def wrapper(*args):
            items = list(args)
            for i, a in enumerate(items):
                if a is None:
                    advanced_log("warning",f"Please enter a value. Returning default")
                    items[i] = 0
                elif not isinstance(a, int):
                    advanced_log("warning", f"Invalid data type, try again.")
                    items[i] = 0
            return func(*items)
        return wrapper
            
    @staticmethod
    @validator
    def left(value):
        return (value, 0, 0, 0)

    @staticmethod
    @validator
    def top(value):
        return (0, value, 0, 0)
    
    @staticmethod
    @validator
    def right(value):
        return (0, 0, value, 0)
    
    @staticmethod
    @validator
    def bottom(value):
        return (0, 0, 0, value)
    
    @staticmethod
    @validator
    def vertical(top, bottom):
        return (0, top, 0, bottom)
    
    @staticmethod
    @validator
    def horizontal(left, right):
        return (left, 0, right, 0)

    @staticmethod
    @validator
    def full(left, top, right, bottom):
        return (left, top, right, bottom)
    
    @staticmethod
    def default():
        return (2, 2, 2, 2)

class Volumes():
    #Core Input
    @staticmethod
    # Can be used as Volumes().marginBuilder(layout, margin_type)
    def marginBuilder(layout, margin_type):
        if layout is None:
            advanced_log("warning",f"Layout is None. Please try again.")
            return None
        
        if isinstance(layout, QLayout):
            layout.setContentsMargins(margin_type)
        else:
            advanced_log("warning",f"Invalid data type: {layout}. Please try again.")

    @staticmethod
    # Can be useed as Volumes().paddingBuilder(layout, value)
    def padding(layout, value):
        if layout is None:
            advanced_log("warning",f"Layout is None, returning None. Please try again.")
            return None
        layout.setSpacing(value)
    
class Widgets():
    @staticmethod
    def application(ui_type, title):
        mw = QMainWindow()
        cw = QWidget()
        cw_layout = QVBoxLayout()

        advanced_log("info",f"Raw ui_type: {class_name(ui_type)}")

        if title is None:
            advanced_log("info",f"Title is None. Setting default title.")
            mw.setWindowTitle("Default Title")
        else:
            cleaned_title = cleaner(title)
            mw.setWindowTitle(cleaned_title)

        if ui_type is None:
            advanced_log("info",f"UI_TYPE is:{class_name(ui_type)}. Skipping")
            pass
        elif isinstance(ui_type, tuple(widgets)):
            advanced_log("info",f"Setting ui_type: {class_name(ui_type)} to {class_name(cw_layout)}")
            cw_layout.addWidget(ui_type)
        else:
            advanced_log("warning","ui_type needs to be a widget excluding (Main Window and App).")

        mw.setGeometry(100,100,400,200)
        advanced_log("info",f"Default App Geometry: (100, 100, 400, 200)")

        advanced_log("info",f"Seting Layout: {class_name(cw_layout)} to {class_name(cw)}.")
        cw.setLayout(cw_layout)

        advanced_log("info",f"Setting Central Widget: {class_name(cw)} to {class_name(mw)}.")
        mw.setCentralWidget(cw)

        if hasattr(mw, "show"):
            advanced_log("info",f"Showing {class_name(mw)}.")
            mw.show()
        else:
            advanced_log("warning",f"{class_name(mw)} does not have the attribure 'show'")
        return mw
    @staticmethod
    def stacked(child):
        spine = QStackedWidget()
        # TODO Check if its None
        if child is None:
            return spine
        
        # TODO Check if its a list/tuple
        if isinstance(child, (list, tuple)):
            # TODO Check if its not () or []
            if not child:
                advanced_log("warning",f"Child list/tuple is empty. Please add a page (child).")
                return spine
            for c in child:
                # TODO Check if its a QWidget
                advanced_log("info",f"Child is {class_name(c)}")
                if isinstance(c, QWidget):
                    advanced_log("info",f"Setting Child widget: {class_name(c)} to {class_name(spine)}")
                    spine.addWidget(c)
                elif isinstance(c, (list, tuple)):
                    advanced_log("warning","Please unpack list/tuple in list/tuple using (*list)")
                else:
                    advanced_log("warning","Core widget for pages should be a QWidget.")
            # TODO Return the stacked widget
            return spine
        elif isinstance(child, QWidget):
            spine.addWidget(child)
            return spine
        else:
            advanced_log("warning",f"Invalid data types entered: {child}. Please try again.")
            return spine
    @staticmethod
    def page(size, child, page_name):
        shell = QWidget()
        layout = QVBoxLayout()
        default_size = (500,300)
        default_text = "Enter Text Here"

        if size is None:
            advanced_log("warning",f"size is None. Returnin default.")
            shell.resize(*default_size)

        if child is None:
            advanced_log("info",f"Child is None. Skipping")  

        if page_name is None:
            advanced_log("warning",f"Page name is None. Returning default.")
            shell.setObjectName(default_text)
        
        if isinstance(size, (list, tuple)):
            advanced_log("info",f"Raw size: {size}")
            verified_size = []
            for integer in size:
                if isinstance(integer, (int, float)):
                    verified_size.append(integer)
                else:
                    shell.resize(*default_size)
                    break
            advanced_log("info",f"Verified size: {verified_size}")
            if len(verified_size) == 2:
                advanced_log("info",f"Fixed Size detected, applying (*{verified_size}).")
                shell.setFixedSize(*verified_size)
            else:
                advanced_log("warning",f"Length of int's is not 2 or 4. Please try again. Setting default.")
                shell.setFixedSize(*default_size)
        
        if isinstance(page_name, str):
            cleaned_name = cleaner(page_name)
            if not cleaned_name:
                shell.setObjectName(default_text)
            else:
                shell.setObjectName(cleaned_name)

        if isinstance(child, (list, tuple)):
            for c in child:
                if isinstance(c, tuple(widgets)):
                    advanced_log("info",f"Adding {class_name(c)} to {class_name(layout)}")
                    layout.addWidget(c)
                else:
                    advanced_log("warning",f"Invalid widget: {class_name(c)}. Child not added.")
        elif isinstance(child, tuple(widgets)):
            layout.addWidget(child)
        else:
            advanced_log("warning",f"Invalid Child instance type. it's currently: {class_name(child)}. Please try again.")
            
        shell.setLayout(layout)
        advanced_log("info",f"Widget Shell is: {class_name(shell)}")
        return shell
    @staticmethod
    def drop_down(child, logic, size):
        instance = QComboBox()
        default_text = "Enter Item Here"

        if logic is None:
            advanced_log("info",f"No logic detected. Skipping")

        if child is None:
            advanced_log("info",f"Child is None. Adding 1 default item to drop down menu.")
            instance.addItem(default_text)
        else:
            if isinstance(child, (list, tuple)):
                if not child:
                    advanced_log("warning",f"List is empty. Adding 1 default item to drop down menu.")
                    instance.addItem(default_text)
                for c in child:
                    if isinstance(c, str):
                        advanced_log("info",f"Adding {c} to {class_name(instance)}")
                        instance.addItem(c)
                    else:
                        advanced_log("warning",f"Invalid Data type: {class_name(c)}. Adding 1 default item to drop down menu.")
                        instance.addItem(default_text)
            else:
                advanced_log("warning","Expecting a list/tuple. Adding 1 default item to drop down menu.")
                instance.addItem(default_text)
        
        Size.set(instance, size)         
        return instance
    @staticmethod
    def widget_shell(alignment, layout, child):
        shell = QWidget()
        default_layout = QVBoxLayout
        if layout is None:
            advanced_log("warning",f"QWidget needs a layout. Setting default. Please try again.")
            shell.setLayout(default_layout())  
        if isinstance(layout, str):
            layout.strip().lower()
            advanced_log("info",f"Raw layout input: {class_name(layout)}.")
            if layout in layouts:
                verified_layout = layouts[layout]()
                advanced_log("info",f"Layout detected: {class_name(verified_layout)}(). Adding it to {class_name(shell)}")
                shell.setLayout(verified_layout)
                Alignment.set(verified_layout, alignment)
                if child is None:
                    advanced_log("warning",f"Child is {class_name(child)}. Widget Shell requires a child.")
                elif isinstance(child, (list, tuple)):
                    for c in child:
                        if isinstance(c, tuple(widgets)):
                            advanced_log("info",f"Widget detected: {class_name(c)}. Adding it to layout")
                            verified_layout.addWidget(c)        
                else:
                    advanced_log("warning",f"Invalid data type: {class_name(child)}. Please try again.")
        else:
            advanced_log("warning",f"Invalid input, please try again.")
        return shell
    @staticmethod
    def label(text):
        instance = QLabel()
        default_text = "Enter Text Here"

        if text is None or text == "":
            advanced_log("info","Text is None or empty. Setting default text.")
            instance.setText(default_text)
        elif isinstance(text, str):
            text = text.strip()
            instance.setText(text)
        else:
            advanced_log("warning",f"Invalid data type: {class_name(text)}. Setting default text")
            instance.setText(default_text)
        return instance
    @staticmethod
    def entry(place_holder):
        instance = QLineEdit()
        
        if place_holder is None or place_holder == "":
            advanced_log("info",f"Placeholder is None or empty. Displaying empty input.")
        elif isinstance(place_holder, str):
            advanced_log("info",f"Placeholder detected. Applying to input.")
            place_holder = place_holder.strip()
            instance.setPlaceholderText(place_holder)
        else:
            advanced_log("warning",f"Placeholder is the wrong data type. Please try again.")
        return instance
    @staticmethod
    def button(text, logic):
        default_text = "Enter Text Here"
        instance = QPushButton()
        
        if text is None:
            advanced_log("info",f"Text is Empty. Returning {default_text}")
            instance.setText(default_text)
        else:
            advanced_log("info",f"Text detected! Adding it to {instance}().")
            instance.setText(text if isinstance(text, str) else default_text)
        
        if logic is None:
            advanced_log("info",f"Logic is None. Skipping.")
        elif callable(logic):
            advanced_log("info",f"Logic detected! Applying logic to {instance}()")
            instance.clicked.connect(logic)
        return instance