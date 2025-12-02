from PyQt6.QtWidgets import (
    QApplication,QMainWindow, QWidget, QStackedWidget, 
    QPushButton, QLabel, QLineEdit, QComboBox, 
    QVBoxLayout, QHBoxLayout, QFormLayout,QLayout
)
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import Qt, QMargins
from PyQt6.QtGui import QFont
from log_util import advanced_log, warning, info, debug, error
from functools import reduce
from api_util import Check
import inspect
import sys 
import os

defaultText = "Enter Text Here"

class Text():
    @staticmethod
    def strip(*text: str) -> list[str]:
        Check.none(text)
        return [t.strip() for t in text]

    @staticmethod
    def lowerCase(*text:str) -> list[str]:
        Check.none(text)
        return [t.lower() for t in text]

    @staticmethod
    def lowerCasedStrip(*text:str) -> list[str]:
        Check.none(text)
        return [t.strip().lower() for t in text]
    
    @staticmethod
    def upperCase(*text:str)-> list[str]:
        Check.none(text)
        return [t.upper() for t in text]
    


class_name = lambda var: var.__class__.__name__
layout_setter = lambda w, l: w.setLayout(l)
widgetType = [
    QWidget, QStackedWidget, QPushButton, 
    QLabel, QLineEdit, QComboBox
]

class Logic():
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
    def set(widget, layoutType):
        Check.none(widget, layoutType)
        verifiedType = layoutType()
        if not isinstance(verifiedType, QLayout):
            raise TypeError(f"{verifiedType} should be a QLayout!")
        try:
            widget.setLayout(verifiedType)
        except Exception as e:
            raise AttributeError(f"Error: {e}")
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
        
                                         
class App():
    def __init__(self, appName:str):
        Check.none(appName)
        Check.String(appName)
        self.appName = Text.lowerCasedStrip(appName)[0]
        advanced_log(info, f"Set app name to: '{self.appName}'")
        self.app = QApplication(sys.argv)
        advanced_log(info, f"Created app instance.")
        self.pageDirectory = {}
        self.window()
        
    def run(self):
        advanced_log(info, f"Executing Application.")
        sys.exit(self.app.exec())
    
    def window(self):
        advanced_log(info, f"Creating Main Window.")
        self.mainWindow = QMainWindow()
        centralWidget = QWidget()
        centralWidgetLayout = QVBoxLayout()
        Size.set(centralWidget, (Size.fill, Size.fill))
        self.mainWindow.setCentralWidget(centralWidget)
        centralWidget.setLayout(centralWidgetLayout)
        self.mainWindow.setWindowTitle(self.appName)
        self.stacked = QStackedWidget()
        advanced_log(info,f"Now supporting pages via: {class_name(self.stacked)}")
        centralWidgetLayout.addWidget(self.stacked)
        advanced_log(info, f"Showing Main Widget")
        self.mainWindow.show()
        return self.mainWindow

    def page(self, pageName: str, pageSize: tuple[int,int] | None = None, fixedSize = False):
        Check.none(pageName)
        cleanedName = Text.lowerCasedStrip(pageName)[0]
        self.pageWidget = QWidget()
        self.pageLayout = QVBoxLayout()
        self.pageWidget.setLayout(self.pageLayout)
        self.pageWidget.setObjectName(cleanedName)
        Size.set(self.pageWidget, (Size.fill, Size.fill))
        advanced_log(info, f"Adding page into stacked widget list.")
        self.stacked.addWidget(self.pageWidget)
        advanced_log(info, f"Setting current page to first page.")
        if pageSize and fixedSize:
            Size.set(self.pageWidget, (Size.fixed, Size.fixed))
            advanced_log(info, f"Setting page size to {pageSize}")
            self.pageWidget.setFixedSize(pageSize[0], pageSize[1])
        self.index = self.stacked.indexOf(self.pageWidget)
        self.stacked.setCurrentIndex(0)
        self.pageDirectory[cleanedName] = {
            "instance" : self.pageWidget,
            "layout" : self.pageLayout,
            "index" : self.index,
            "pageChildren" : {}
        }
        self.currentPage = cleanedName
        advanced_log(info, f"Creating page: {cleanedName} for {self.appName}")
        return self.pageWidget

    def widgetShell(self, widgetName: str, layout, size: tuple[int,int] | None = None,  alignment= None, fixedSize = False):
        self.pageInfo = self.pageDirectory[self.currentPage] # pageDirectory[curentPage](options: [1. Widget], [2. Layouts], [Children])
        pageLayout = self.pageInfo["layout"] # Parent Layout
        instance = QWidget()
        Check.none(layout)
        verifiedLayout = Layout.set(instance, layout) 
        if alignment: 
            Alignment.set(verifiedLayout, alignment)
        if fixedSize and size:
            Size.set(instance, (Size.fixed, Size.fixed))
            advanced_log(info, f"Size detected, setting as {size}")
            instance.setFixedSize(size[0], size[1])
        instance.setObjectName(widgetName)
        pageLayout.addWidget(instance)
        self.pageInfo["pageChildren"][widgetName]= {
            "shellInstance" : instance,
            "shellLayout" : verifiedLayout,
            "shellName" : widgetName,
            "shellChildren" : {}
        }
        advanced_log(info, f"Creating widgetShell for {self.pageInfo}")
        return instance
    
    def formItems(self, formName:str, layout,size: tuple[int,int] | None = None,  alignment= None, fixedSize = False ):
        self.shellInfo = self.pageInfo["pageChildren"][formName]
        formLayout = self.shellInfo["shellLayout"]
        instance = QWidget()
        Check.none(layout)
        verifiedLayout = Layout.set(instance, layout)
        if alignment: 
            Alignment.set(verifiedLayout, alignment)
        if fixedSize and size:
            Size.set(instance, (Size.fixed, Size.fixed))
            advanced_log(info, f"Size detected, setting as {size}")
            instance.setFixedSize(size[0], size[1])
        formLayout.addItem(instance)
        self.shellInfo["shellChildren"] ={
            "children" : instance,
        }
    
    def label(self,shellName:str , widgetName:str, text:str, size: int | None):
        currentShell = self.pageInfo["pageChildren"][shellName]
        shellLayout = self.pageInfo["pageChildren"][shellName]["shellLayout"]
        cleanedText = Text.strip(text)[0]
        instance = QLabel()
        instance.setText(cleanedText)
        font = QFont()
        if size:
            font.setPointSize(size)
        instance.setFont(font)
        advanced_log(debug, f"Adding label to {shellName}")
        shellLayout.addWidget(instance)
        currentShell["shellChildren"][widgetName] = { 
            "labelInstance" : instance,
            "labelText" : cleanedText
        }
        advanced_log(info, f"Creating Label for {currentShell}")
        return instance

    def drop_down(self,shellName, text:list | tuple, logic, widgetName: str):
        currentShell = self.pageInfo["pageChildren"][shellName]
        shellLayout = currentShell["shellLayout"]
        instance = QComboBox()
        if logic:
            pass
        instance.addItems(text)
        shellLayout.addWidget(instance)
        currentShell["shellChildren"][widgetName] = { 
            "dropDownInstance" : instance,
            "dropDownText" : text
        }
        return instance

    def lineEdit(self, shellName,  placeHolder: str, widgetName:str, hidden = False):
        currentShell = self.pageInfo["pageChildren"][shellName]
        shellLayout = currentShell["shellLayout"]
        instance = QLineEdit()
        cleanedPlaceHolder = Text.strip(placeHolder)[0]
        instance.setPlaceholderText(cleanedPlaceHolder)
        shellLayout.addWidget(instance)
        if hidden:
            instance.setEchoMode(QLineEdit.EchoMode.Password)
        currentShell["shellChildren"][widgetName] = { 
            "lineEditInstance" : instance,
            "placeHolder" : placeHolder
        }
        return instance

    def button(self, shellName, text: str, logic, widgetName:str, dummy = False):
        currentShell = self.pageInfo["pageChildren"][shellName]
        shellLayout = currentShell["shellLayout"]
        if not dummy:
            Check.Callable(logic)
        instance = QPushButton()
        cleanedText = Text.strip(text)[0]
        instance.setText(cleanedText)
        shellLayout.addWidget(instance)
        if not dummy:
            instance.clicked.connect(logic)
        currentShell["shellChildren"][widgetName] = { 
            "buttonInstance" : instance,
            "buttonText" : text
        }
        return instance
