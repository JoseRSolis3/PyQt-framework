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
def cleaner(text: str) -> str:
    return text.strip()
def loweredCleaner(text:str)->str:
    return text.strip().lower()

class_name = lambda var: var.__class__.__name__
layout_setter = lambda w, l: w.setLayout(l)
widgetType = [
    QWidget, QStackedWidget, QPushButton, 
    QLabel, QLineEdit, QComboBox
]

class Library():
    def __init__(self) -> None:
        self.widgetDirectory = {}
        self.layoutDirectory = {}
        self.comboTextDirectory = {}
        self.pageDirectory = {}

    def startsWith(self, widgetName: str, userInput: str) -> bool:
        cleanedName = cleaner(userInput)
        return widgetName.startswith(cleanedName)
    
    def widgetRegistration(self, widgetName:str, widget):
        Check.none(widgetName, widget)
        Check.String(widgetName)
        cleanedName = cleaner(widgetName)
        if cleanedName not in self.widgetDirectory:
            self.widgetDirectory[cleanedName] = widget
        else:
            raise KeyError(f"{cleanedName} already exists!")

    def layoutRegistration(self, widgetName:str, layout):
        Check.none(widgetName, layout)
        Check.String(widgetName)
        cleanedName = cleaner(widgetName)
        if cleanedName not in self.layoutDirectory:
            self.layoutDirectory[cleanedName] = layout
        else:
            raise KeyError(f"{cleanedName} already exists!")
    
    def pageRegistry(self, pageName:str, page: QWidget):
        Check.none(pageName, page)
        Check.String(pageName)
        cleanedName = cleaner(pageName)
        if cleanedName not in self.pageDirectory:
            self.pageDirectory[cleanedName] = page
        else:
            raise KeyError(f"{cleanedName} already exists!")
    
    def lookup(self, widgetName: str, layout: bool = False, widget: bool = False):
        Check.none(widgetName)
        Check.String(widgetName)
        cleanedName = loweredCleaner(widgetName)
        if layout and widget:
            if cleanedName in self.layoutDirectory and cleanedName in self.widgetDirectory:
                widgetInstance = self.widgetDirectory[cleanedName]
                layoutInstance = self.layoutDirectory[cleanedName]
                return (widgetInstance, layoutInstance)
            else:
                missing = []
                if cleanedName not in self.widgetDirectory:
                    missing.append(cleanedName)
                if cleanedName not in self.layoutDirectory:
                    missing.append(cleanedName)
                raise KeyError(f"Missing: {missing}.")
        if layout:
            if cleanedName in self.layoutDirectory:
                return self.layoutDirectory[cleanedName]
            else:
                raise KeyError(f"{cleanedName} does not exist!")
        if widget:
            if cleanedName in self.widgetDirectory:
                return self.widgetDirectory[cleanedName]
            else:
                raise KeyError(f"{cleanedName} does not exist!")
        
    def comboTextRegistration(self, widgetName: str, text: list | tuple):
        Check.none(widgetName, text)
        verifiedText = []
        cleanedName = cleaner(widgetName)
        for item in text:
            Check.String(item)
            verifiedText.append(item)
        if cleanedName not in self.comboTextDirectory:
            self.comboTextDirectory[cleanedName] = verifiedText
        else:
            raise KeyError(f"{cleanedName} already exists!")
        return self.comboTextDirectory[cleanedName]
        
universalLibrary = Library()

class Logic():
    @staticmethod
    def currentIndex(widget: QStackedWidget | QComboBox, index: int):
        Check.none(widget)
        Check.Number(index)
        if isinstance(widget, (QStackedWidget, QComboBox)):
            advanced_log("info",f"Verified, widget = {class_name(widget)}. Continuing to index verification.")
            try:
                advanced_log("info",f"Verified, index = {class_name(index)}. Continuing to set logic.")
                widget.setCurrentIndex(index)
            except IndexError:
                advanced_log("warning",f"Index is out of bounds.")
            except Exception as e:
                advanced_log("error",f"Error - {e}")
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
        Check.none(widget, objectName)
        Check.String(objectName)
        cleanedName = cleaner(objectName)
        widget.setObjectName(cleanedName)

class Children():
    @staticmethod
    def set(parent, child: tuple | list):
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

        mainWindow = QMainWindow()
        centralWidget = QWidget()
        centralWidgetLayout = QVBoxLayout()
        mainWindow.setGeometry(100,100,400,200)
        mainWindow.setCentralWidget(centralWidget)
        centralWidget.setLayout(centralWidgetLayout)
        universalLibrary.widgetRegistration("mainWindow", mainWindow)

        Check.none(uiType, title)
        Check.String(title)
        cleanedTitle = cleaner(title)
        mainWindow.setWindowTitle(cleanedTitle)
        universalLibrary.widgetRegistration("centralWidget", centralWidget)
        universalLibrary.layoutRegistration("centralWidget", centralWidgetLayout)

        Check.Tuple(uiType)
        centralWidgetLayout.addWidget(uiType)
        Size.set(centralWidget, (Size.fill, Size.fill))
        mainWindow.show()
        return mainWindow
     
    @staticmethod
    def stacked(child):
        Check.none(child)
        instance = QStackedWidget()
        Children.set(instance, child)
        universalLibrary.widgetRegistration("stack", instance)
        return instance
    
    @staticmethod
    def page(parentWidgetName:str, size: list | tuple, pageName: str):
        Check.none(parentWidgetName, size, pageName)
        for n in size:
            Check.Number(n, decimal=True)
        cleanedName = cleaner(pageName)
        instance = QWidget()
        layout = QVBoxLayout()
        instance.setLayout(layout)
        universalLibrary.pageRegistry(pageName, instance)
        universalLibrary.layoutRegistration(pageName, layout)
        Size.set(instance, size)
        instance.setObjectName(cleanedName)
        parentFound = universalLibrary.layoutDirectory[parentWidgetName]
        parentFound.addWidget(instance)
        return instance
    
    @staticmethod
    def drop_down(parentWidgetName:str, text:list | tuple, logic, size: list | tuple, widgetName: str):
        Check.none(parentWidgetName, text, widgetName)
        Check.String(widgetName)
        cleanedName = loweredCleaner(widgetName)
        instance = QComboBox()
        if logic:
            pass
        instance.addItems(text)
        universalLibrary.widgetRegistration(cleanedName, instance)
        universalLibrary.comboTextRegistration(cleanedName, text)
        Size.set(instance, size)        
        parentFound = universalLibrary.layoutDirectory[parentWidgetName]
        parentFound.addWidget(instance)
        return instance
    
    @staticmethod
    def widget_shell(parentWidgetName, layout, alignment, widgetName: str):
        Check.none(parentWidgetName, layout, alignment, widgetName)
        Check.String(widgetName)
        shell = QWidget()
        verifiedLayout = Layout.set(shell, layout) 
        if alignment: 
            Alignment.set(verifiedLayout, alignment)
        shell.setObjectName(widgetName)
        universalLibrary.widgetRegistration(widgetName, shell)
        universalLibrary.layoutRegistration(widgetName, verifiedLayout)
        parentFound = universalLibrary.layoutDirectory[parentWidgetName]
        parentFound.addWidget(shell)
        return shell
        
    @staticmethod
    def label(parentLayout, text:str):
        Check.none(parentLayout, text)
        Check.String(text)
        cleanedText = cleaner(text)
        instance = QLabel()
        instance.setText(cleanedText)
        parentLayout.addWidget(instance)
        return instance
        
    @staticmethod
    def entry(parentLayout, placeHolder: str):
        Check.none(parentLayout, placeHolder)
        Check.String(placeHolder)
        instance = QLineEdit()
        cleanedPlaceHolder = cleaner(placeHolder)
        instance.setPlaceholderText(cleanedPlaceHolder)
        parentLayout.addWidget(instance)
        return instance
    
    @staticmethod
    def button(parentLayout, text: str, logic):
        Check.none(parentLayout, text)
        Check.Callable(logic)
        Check.String(text)
        instance = QPushButton()
        cleanedText = cleaner(text)
        instance.setText(cleanedText)
        parentLayout.addWidget(instance)
        instance.clicked.connect(logic)
        return instance