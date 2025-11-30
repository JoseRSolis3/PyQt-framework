from PyQt6.QtWidgets import (
    QApplication,QMainWindow, QWidget, QStackedWidget, 
    QPushButton, QLabel, QLineEdit, QComboBox, 
    QVBoxLayout, QHBoxLayout, QFormLayout,QLayout
)
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import Qt, QMargins
from PyQt6.QtGui import QFont
from log_util import advanced_log
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
    
    def pageRegistry(self, page: dict):
        Check.none(page)
        Check.Dictionary(page)
        for pageName, pageWidget in page.items():
            advanced_log("info",f"Adding: [stack]('{pageName}' : {class_name(pageWidget)})")
            cleanedName = cleaner(pageName)
            if "stack" not in self.pageDirectory:
                advanced_log("info",f"'stack' does not exist, setting up dict [stack]")
                self.pageDirectory["stack"] = {}
            if cleanedName not in self.pageDirectory:
                self.pageDirectory["stack"][cleanedName] = pageWidget
                advanced_log("info",f"Current Page Directory: {self.pageDirectory["stack"]}")
            else:
                raise KeyError(f"{cleanedName} already exists!")
    
    def lookup(self, widgetName: str, layout: bool = False, widget: bool = False, page = False):
        Check.none(widgetName)
        Check.String(widgetName)
        cleanedName = cleaner(widgetName)
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
        if page:
            if cleanedName in self.pageDirectory["stack"]:
                return self.pageDirectory["stack"][cleanedName]
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
    def findIndex(pageName: str):
        Check.none(pageName)
        cleanedName = cleaner(pageName)
        pages = universalLibrary.pageDirectory["stack"]
        advanced_log("info",f"pages = {pages}")
        stackWidget = universalLibrary.widgetDirectory["stack"]
        advanced_log("info",f"stackWidget = {stackWidget}")
        pageWidget = pages[cleanedName]
        advanced_log("info",f"pageWidget = {pageWidget}")
        index = stackWidget.indexOf(pageWidget)
        advanced_log("info", f"Index of {cleanedName} in stack: {index}")
        return index

    @staticmethod
    def currentIndex(pageName: str):
        Check.none(pageName)
        Check.String(pageName)
        widget = universalLibrary.widgetDirectory["stack"]
        universalLibrary.lookup(pageName, page=True)
        page = universalLibrary.pageDirectory["stack"][pageName]
        pageIndex = widget.indexOf(page)
        if isinstance(widget, (QStackedWidget, QComboBox)):
            advanced_log("info",f"Verified, widget = {class_name(widget)}. Continuing to index verification.")
            try:
                advanced_log("info",f"Verified, index = {pageIndex}. Continuing to set logic.")
                widget.setCurrentIndex(pageIndex)
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
    
class Widgets():
    @staticmethod
    def application(uiType, title: str):
        mainWindow = QMainWindow()
        centralWidget = QWidget()
        centralWidgetLayout = QVBoxLayout()
        mainWindow.setGeometry(100,100,500,300)
        Size.set(centralWidget, (Size.fill, Size.fill))
        mainWindow.setCentralWidget(centralWidget)
        centralWidget.setLayout(centralWidgetLayout)
        advanced_log("info",f"Set {class_name(mainWindow)} with a {class_name(centralWidget)}. It has a {class_name(centralWidgetLayout)} with a default geometry of (100,100,400,200)")
        universalLibrary.widgetRegistration("mainWindow", mainWindow)
        advanced_log("info",f"Registered {class_name(mainWindow)} as mainWindow")

        Check.none(uiType, title)
        Check.String(title)
        cleanedTitle = cleaner(title)
        mainWindow.setWindowTitle(cleanedTitle)
        universalLibrary.widgetRegistration("centralWidget", centralWidget)
        advanced_log("info",f"Registered {class_name(centralWidget)} as centralWidget")
        universalLibrary.layoutRegistration("centralWidget", centralWidgetLayout)
        advanced_log("info",f"Registered {class_name(centralWidgetLayout)} as centralWidget")

        Check.Tuple(uiType)
        for widget in uiType:
            instance = universalLibrary.widgetDirectory[widget]
            centralWidgetLayout.addWidget(instance)
            advanced_log("info",f"Added {class_name(widget)} to {class_name(centralWidgetLayout)}")
        Size.set(centralWidget, (Size.fill, Size.fill))
        mainWindow.show()
        return mainWindow
     
    @staticmethod
    def stacked():
        instance = QStackedWidget()
        layout = QVBoxLayout()
        universalLibrary.widgetRegistration("stack", instance)
        advanced_log("info",f"Registered {class_name(instance)} as stack")
        universalLibrary.layoutRegistration("stack", layout)
        advanced_log("info",f"Registered {class_name(layout)} as stack")
        return instance
    
    @staticmethod
    def page(pageName: str):
        Check.none(pageName)
        cleanedName = cleaner(pageName)
        instance = QWidget()
        layout = QVBoxLayout()
        instance.setLayout(layout)
        instance.setObjectName(cleanedName)
        Size.set(instance, (Size.fill, Size.fill))
        stackedWidget = universalLibrary.widgetDirectory["stack"]
        stackedWidget.addWidget(instance)
        advanced_log("info",f"Added {pageName} to {class_name(stackedWidget)}")
        universalLibrary.pageRegistry({pageName:instance})
        advanced_log("info",f"Registered Page as {pageName}")
        universalLibrary.layoutRegistration(pageName, layout)
        advanced_log("info",f"Registered Layout as {pageName}")
        return instance
    
    @staticmethod
    def drop_down(parentName:str, text:list | tuple, logic, size: list | tuple, widgetName: str):
        Check.none(parentName, text, widgetName)
        Check.String(widgetName)
        cleanedName = loweredCleaner(widgetName)
        instance = QComboBox()
        if logic:
            pass
        instance.addItems(text)
        Size.set(instance, size)        
        parentLayout = universalLibrary.layoutDirectory[parentName]
        parentLayout.addWidget(instance)
        advanced_log("info",f"Added {widgetName} to {parentName} with the items: {text}")
        universalLibrary.widgetRegistration(widgetName, instance)
        advanced_log("info",f"Registered {class_name(instance)} as {widgetName}")
        universalLibrary.comboTextRegistration(cleanedName, text)
        advanced_log("info",f"Registered items: {text}")
        return instance
    
    @staticmethod
    def widget_shell(parentName, layout, alignment, widgetName: str):
        Check.none(parentName, layout, alignment, widgetName)
        Check.String(widgetName)
        instance = QWidget()
        verifiedLayout = Layout.set(instance, layout) 
        if alignment: 
            Alignment.set(verifiedLayout, alignment)
        instance.setObjectName(widgetName)
        parentLayout = universalLibrary.layoutDirectory[parentName]
        parentLayout.addWidget(instance)
        advanced_log("info",f"Added {widgetName} to {parentName}")
        universalLibrary.widgetRegistration(widgetName, instance)
        universalLibrary.layoutRegistration(widgetName, verifiedLayout)
        advanced_log("info",f"Registered {class_name(instance)} as {widgetName}")
        return instance
        
    @staticmethod
    def label(parentName:str, text:str, widgetName:str, size: int | None):
        Check.none(parentName, text, widgetName)
        Check.String(parentName, text, widgetName)
        Check.Number(size, exception=True)
        cleanedText = cleaner(text)
        instance = QLabel()
        instance.setText(cleanedText)
        font = QFont()
        if size:
            font.setPointSize(size)
        instance.setFont(font)
        universalLibrary.lookup(parentName, layout=True)
        parentLayout = universalLibrary.layoutDirectory[parentName]
        parentLayout.addWidget(instance)
        advanced_log("info",f"Added {widgetName} to {parentName} with the text: {cleanedText}")
        universalLibrary.widgetRegistration(widgetName, instance)
        advanced_log("info",f"Registered {class_name(instance)} as {widgetName}")
        return instance
        
    @staticmethod
    def entry(parentName:str, placeHolder: str, widgetName:str, hidden = False):
        Check.none(parentName, placeHolder, widgetName)
        Check.String(parentName,placeHolder, widgetName)
        instance = QLineEdit()
        cleanedPlaceHolder = cleaner(placeHolder)
        instance.setPlaceholderText(cleanedPlaceHolder)
        if hidden:
            instance.setEchoMode(QLineEdit.EchoMode.Password)
        universalLibrary.lookup(parentName, layout=True)
        parentLayout = universalLibrary.layoutDirectory[parentName]
        parentLayout.addWidget(instance)
        advanced_log("info",f"Added {widgetName} to {parentName} with the placeholder: {cleanedPlaceHolder}")
        universalLibrary.widgetRegistration(widgetName, instance)
        advanced_log("info",f"Registered {class_name(instance)} as {widgetName}")
        return instance
    
    @staticmethod
    def button(parentName, text: str, logic, widgetName:str, dummy = False):
        Check.none(parentName, text, widgetName)
        if not dummy:
            Check.Callable(logic)
        Check.String(text, widgetName)
        instance = QPushButton()
        cleanedText = cleaner(text)
        instance.setText(cleanedText)
        universalLibrary.lookup(parentName, layout=True)
        parentLayout = universalLibrary.layoutDirectory[parentName]
        parentLayout.addWidget(instance)
        if not dummy:
            instance.clicked.connect(logic)
        advanced_log("info",f"Added {widgetName} to {parentName} with the Text: {cleanedText}")
        universalLibrary.widgetRegistration(widgetName, instance)
        advanced_log("info",f"Registered {class_name(instance)} as {widgetName}")
        return instance
    
class App():
    @staticmethod
    def Initialize(appName:str):
        Check.none(appName)
        Check.String(appName)
        cleanedName = cleaner(appName)
        app = QApplication(sys.argv)
        advanced_log("info",f"Initializing: {class_name(app)}")
        universalLibrary.widgetRegistration(cleanedName, app)
        advanced_log("info",f"Registered: {class_name(app)} as {cleanedName}")
        return app
    
    @staticmethod
    def run(appName):
        Check.none(appName)
        universalLibrary.lookup(appName,widget=True)
        app = universalLibrary.widgetDirectory[appName]
        if not isinstance(app, QApplication):
            raise ValueError(f"{app} is not a QApplication!")
        advanced_log("info",f"Running application.")
        sys.exit(app.exec())