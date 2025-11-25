from PyQt6.QtWidgets import (
    QApplication,QMainWindow, QWidget, QStackedWidget, 
    QPushButton, QLabel, QLineEdit, QComboBox, 
    QVBoxLayout, QHBoxLayout, QFormLayout,QLayout
)
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import Qt, QMargins
from log_util import advanced_log
from functools import reduce
from api_util import Check
import inspect
import sys 
import os

defaultText = "Enter Text Here"
cleaner = lambda var: var.strip()
class_name = lambda var: var.__class__.__name__
layout_setter = lambda w, l: w.setLayout(l)
widgetType = [
    QWidget, QStackedWidget, QPushButton, 
    QLabel, QLineEdit, QComboBox
]

class Logic():
    @staticmethod
    def currentIndex(widget: QStackedWidget | QComboBox, index: int):
        if widget is None or index is None:
            advanced_log("warning",f"input is None. Returning None.")
            return None
        if isinstance(widget, (QStackedWidget, QComboBox)):
            advanced_log("info",f"Verified, widget = {class_name(widget)}. Continuing to index verification.")
            if isinstance(index, int):
                try:
                    advanced_log("info",f"Verified, index = {class_name(index)}. Continuing to set logic.")
                    widget.setCurrentIndex(index)
                except IndexError:
                    advanced_log("warning",f"Index is out of bounds.")
                except Exception as e:
                    advanced_log("error",f"Error - {e}")
            else:
                advanced_log("warning",f"Invalid data type for index")
                return None
        else:
            advanced_log("warning",f"Invalid data type for widget")
            return None

    @staticmethod
    def clicked(widget: QPushButton, action):
        if action is None:
            advanced_log("warning",f"Action is None. Returning None")
            return None
        elif isinstance(widget, QPushButton):
            advanced_log("info",f"Widget is {class_name(widget)}")
            widget.clicked.connect(action)
        else:
            advanced_log("warning",f"Wrong widget for logic. Widget is not a button.")
    
    @staticmethod
    def activatedCombobox(widget: QComboBox, action, returnText = True):
        if action is None:
            advanced_log("warning",f"Action is None. Returning None")
            return None
        if isinstance(widget, QComboBox):
            advanced_log("info",f"Widget is {class_name(widget)}")
            if returnText:
                advanced_log("info",f"Connecting activated signal to return selected text (str).")
                widget.activated[str].connect(action)
            elif not returnText:
                advanced_log("info",f"Connecting activated signal to return selected index (int).")
                widget.activated[int].connect(action)
        else:
            advanced_log("warning",f"Wrong widget for logic. Widget is not a drop box.")
        
    @staticmethod
    def activatedPages(list, pageName, action):
        variables = [list, pageName, action]
        for var in variables:
            if var is None:
                advanced_log("warning",f"{var} is None. returning None.")
                return None
        

class ObjectName():
    @staticmethod
    def set(widget, objectName):
        if objectName is None:
            advanced_log("warning",f"Object Name is empty. Setting default.")
            widget.setObjectName(defaultText)
        elif not isinstance(objectName, str):
            advanced_log("warning",f"Invalid data type: {class_name(objectName)}. Setting default.")
            widget.setObjectName(defaultText)
        else:
            advanced_log("info",f"Verified. Setting {objectName}.")
            cleaned_name = cleaner(objectName)
            widget.setObjectName(cleaned_name)

class Children():
    @staticmethod
    def set(parent, child):
        advanced_log("info",f"Raw Input: [parent = {class_name(parent)}] [child = {class_name(child)}]")
        Check.none(parent, child)
        if isinstance(child, (tuple, list)):
            advanced_log("info", f"Multiple children detected.")
            for c in child:
                if not isinstance(c, (tuple(widgetType), str)):
                    advanced_log("warning",f"Invalid data type for child. Setting default.")
                    if isinstance(parent, QComboBox):
                        advanced_log("info",f"Adding {class_name(c)} to {class_name(parent)}.")
                        parent.addItem(defaultText)
                    elif isinstance(parent, QStackedWidget):
                        advanced_log("info",f"Adding {class_name(c)} to {class_name(parent)}.")
                        parent.addWidget(QWidget())
                    elif isinstance(parent, QLayout):
                        advanced_log("info",f"Adding {class_name(c)} to {class_name(parent)}.")
                        parent.addWidget(QWidget())
                else:
                    advanced_log("info",f"Verified. Adding {class_name(c)}")
                    if isinstance(parent, QComboBox):
                        advanced_log("info",f"Adding {class_name(c)} to {class_name(parent)}.")
                        parent.addItem(c)
                    elif isinstance(parent, QStackedWidget):
                        advanced_log("info",f"Adding {class_name(c)} to {class_name(parent)}.")
                        parent.addWidget(c)
                    else:
                        advanced_log("info",f"Adding {class_name(c)} to {class_name(parent)}.")
                        parent.addWidget(c)
        else:
            advanced_log("info",f"Verified. Adding {class_name(child)}.")
            if isinstance(parent, QComboBox):
                parent.addItem(child)
            else:
                parent.addWidget(child)

class Size():
    auto = QSizePolicy.Policy.Preferred
    fill = QSizePolicy.Policy.Expanding
    fixed = QSizePolicy.Policy.Fixed
    min = QSizePolicy.Policy.Minimum
    max = QSizePolicy.Policy.Maximum
    stretch = QSizePolicy.Policy.Expanding
    default = QSizePolicy.Policy.Expanding

    @staticmethod
    def set(widget, sizeStyle: tuple | list):
        Check.none(widget, sizeStyle)
        if not isinstance(sizeStyle, (tuple, list)):
            advanced_log("warning",f"Invalid data type: size = {class_name(sizeStyle)}. Returning default.")
            return widget.setSizePolicy(Size.default, Size.default)
        else:
            items = list(sizeStyle)
            isInteger = False
            for i, style in enumerate(sizeStyle):
                if isinstance(style, int):
                    advanced_log("info",f"Fixed size detected. applying {style}")
                    isInteger = True
                    items[i] = style
                elif isinstance(style, QSizePolicy.Policy):
                    advanced_log("info",f"Style is {class_name(style)}. Applying {style} to {class_name(widget)}")
                    items[i] = style                    
                else:
                    advanced_log("warning",f"Invalid data type: style = {class_name(style)}. Data type accepted is QSizePolicy. Returning default.")
                    items[i] = Size.default
            if isInteger == True:
                widget.setSizePolicy(Size.fixed,Size.fixed)
                widget.resize(*items)
                advanced_log("info",f"Resize: {items}")
            else:
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
    def set(layout, alignmentFlag):
        advanced_log("debug",f"Raw data types: [layout:{layout} = {class_name(layout)}] [alignmentFlag: {alignmentFlag} = {class_name(alignmentFlag)}]")
        if alignmentFlag is None:
            advanced_log("warning",f"Alignment is None. Setting default.")
            layout.setAlignment(Alignment.default)
        elif isinstance(alignmentFlag, Qt.AlignmentFlag):
            advanced_log("info",f"Verified: AlignmentFlag = {class_name(alignmentFlag)}.")
            layout.setAlignment(alignmentFlag)
        else:
            advanced_log("warning",f"Invalid data type. Setting default.")
            layout.setAlignment(Alignment.default)

class Layout():
    vertical = QVBoxLayout
    horizontal = QHBoxLayout
    form = QFormLayout
    default = QVBoxLayout

    @staticmethod
    def set(widget, type):
        advanced_log("info",f"Raw input: [widget = {class_name(widget)}] [type = {class_name(type)}]")
        if type is None:
            advanced_log("warning",f"Layout type needs to have a value. Setting default.")
            widget.setLayout(Layout.default())
            return widget.layout()        
        try:
            advanced_log("info",f"Before instantiating: {type} = {class_name(type)}")
            verifiedType = type()
            advanced_log("info",f"After instantiating: {verifiedType} = {class_name(verifiedType)}") 
            if isinstance(verifiedType, QLayout):
                widget.setLayout(verifiedType)
                advanced_log("info",f"Returning: {class_name(widget.layout())}")
                return widget.layout()
        except:
            type = Layout.default()
            if isinstance(type, QLayout):
                widget.setLayout(type)
                advanced_log("info",f"Returning: {class_name(widget.layout())}")
                return widget.layout()
        
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

    @staticmethod
    def set(layout, type):
        return layout.setContentsMargins(type)
    
class Padding():
    @staticmethod
    def set(layout, value):
        if not isinstance(value, int):
            advanced_log("warning",f"Invalid data type. Returning Default.")
            return 2
        else:
            return layout.setSpacing(value)
    
class Widgets():
    @staticmethod
    def application(uiType, title: str):
        print("\n")
        mainWindow = QMainWindow()
        centralWidget = QWidget()
        centralWidgetLayout = QVBoxLayout()
        mainWindow.setGeometry(100,100,400,200)
        mainWindow.setCentralWidget(centralWidget)
        centralWidget.setLayout(centralWidgetLayout)
        advanced_log("debug",f"Raw Input: [{uiType} = {class_name(uiType)}] [{title} = {class_name(title)}]")

        Check.none(uiType, title)
        Check.String(title)
        cleanedTitle = cleaner(title)
        advanced_log("info",f"Verified! Setting title to: {cleanedTitle}")
        mainWindow.setWindowTitle(cleanedTitle)

        if not isinstance(uiType, tuple(widgetType)):
            advanced_log("warning",f"invalid data type! Expected: QWidgets. Entered: {class_name(uiType)}. Retruning stacked.")
            centralWidgetLayout.addWidget(QStackedWidget())
        else:
            advanced_log("info",f"Verified! Setting uiType to {class_name(uiType)}")
            centralWidgetLayout.addWidget(uiType)

        Size.set(centralWidget, (Size.fill, Size.fill))
        advanced_log("info",f"Showing application.")
        mainWindow.show()
        return mainWindow
     
    @staticmethod
    def stacked(child: QWidget):
        print("\n")
        instance = QStackedWidget()
        Children.set(instance, child)
        return instance
    
    @staticmethod
    def page(size: list | tuple, child, page_name: str):
        shell = QWidget()
        layout = QVBoxLayout()
        shell.setLayout(layout)
        Size.set(shell, size)
        ObjectName.set(shell, page_name) 
        advanced_log("debug",f"Children.set({layout}, {child})")
        Children.set(layout, child)         
        return shell
    
    @staticmethod
    def drop_down(child, logic, size: list | tuple):
        instance = QComboBox()
        if logic is None:
            advanced_log("info",f"No logic detected. Skipping")
        Children.set(instance, child)
        Size.set(instance, size)        
        return instance
    
    @staticmethod
    def widget_shell(layout, alignment, child):
        print("\n")
        advanced_log("info",f"Raw Input: [{layout} = {class_name(layout)}] [{alignment} = {class_name(alignment)}] [{child} = {class_name(child)}]")
        shell = QWidget()

        advanced_log("info",f"layout = Layout.set(shell, layout) -> layout = {class_name(layout)}")  
        verifiedLayout = Layout.set(shell, layout)  

        advanced_log("info",f"Alignment.set(verifiedLayout, alignment) -> Alignment.set({class_name(verifiedLayout)}, {class_name(alignment)})")
        Alignment.set(verifiedLayout, alignment)

        advanced_log("info",f"Children.set(verifiedLayout, child) -> Children.set({class_name(verifiedLayout)}, {class_name(child)})")
        Children.set(verifiedLayout, child)

        advanced_log("info",f"Verified Input: [{layout} = {class_name(verifiedLayout)}] [{alignment} = {class_name(alignment)}] [{child} = {class_name(child)}]")
        return shell
        
    @staticmethod
    def label(text):
        instance = QLabel()
        default_text = "Enter Text Here"

        if text is None or text == "":
            advanced_log("info","Text is None or empty. Setting default text.")
            instance.setText(default_text)
        elif isinstance(text, str):
            cleanedText = cleaner(text)
            instance.setText(cleanedText)
        else:
            advanced_log("warning",f"Invalid data type: {class_name(text)}. Setting default text")
            instance.setText(default_text)
        return instance
    
    @staticmethod
    def entry(placeHolder):
        instance = QLineEdit()
        
        if placeHolder is None or placeHolder == "":
            advanced_log("info",f"Placeholder is None or empty. Displaying empty input.")
        elif isinstance(placeHolder, str):
            advanced_log("info",f"Placeholder detected. Applying to input.")
            cleanedPlaceHolder = cleaner(placeHolder)
            instance.setPlaceholderText(cleanedPlaceHolder)
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
            advanced_log("info",f"Logic is None.")
        elif callable(logic):
            advanced_log("info",f"Logic detected! Applying logic to {instance}()")
            instance.clicked.connect(logic)
        return instance