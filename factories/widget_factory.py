from PyQt6.QtWidgets import (
    QApplication,QMainWindow, QWidget, QStackedWidget,
    QPushButton, QLabel, QLineEdit, QComboBox,
    QVBoxLayout, QHBoxLayout, QFormLayout
)

from PyQt6.QtCore import Qt

from log_util import log

import inspect
import sys
import os

verifier_name = lambda v: f"|{v.upper()} VERIFIER|"
builder_name = lambda b: f"|{b.upper()} BUILDER|"

class_name = lambda w: w.__class__.__name__
reminder = "|**REMINDER**|"
default_text = "Enter Text Here"
lower_strip = lambda t: t.strip().lower() if isinstance(t, str) else t
strip = lambda t: t.strip() if isinstance(t, str) else t

def divider_wrapper(char="=", length=20):
    def decorator(func):
        def wrapper(*args, **kwargs):
            line = char * length
            print(line)
            result = func(*args, **kwargs)
            print(line)
            return result
        return wrapper
    return decorator


class widgetFactory:
    def __init__(self):
        self.widgets_with_text = {
            "label" : QLabel,
            "button" : QPushButton,
            "input" : QLineEdit,
            "dropdown" : QComboBox,
        }

        self.widgets_without_text = {
            "widget" : QWidget,
            "stacked" : QStackedWidget,
            "main window" : QMainWindow,
        }

        self.layouts = {
            "vertical" : QVBoxLayout,
            "horizontal" : QHBoxLayout,
            "form" : QFormLayout
        }

        self.alignments = {
            "left" : Qt.AlignmentFlag.AlignLeft,
            "right" : Qt.AlignmentFlag.AlignRight,
            "top" : Qt.AlignmentFlag.AlignTop,
            "bottom" : Qt.AlignmentFlag.AlignBottom,
            "center" : Qt.AlignmentFlag.AlignCenter,
        }

        self.logic_attributes = {
            "clicked" : lambda w: w.on_click,
            # TODO: Allow for text edit via GUI
        }

    def widget_verifier(self, widget = None):
        v = "widget"
        log.info(f"{verifier_name(v)}: Entered value is ({widget} and its instance is ({class_name(widget)}))")

        if widget is None:
            log.warning(f"{verifier_name(v)}: widget is None. Please enter a valid entry.")
            return None
        elif widget == "":
            log.warning(f"{verifier_name(v)}: Widget initiated but left blank. Please try again. Returning None.")
            return None
        elif not isinstance(widget, str):
            log.warning(f"{verifier_name(v)}: Data type needs to be 'str'. Please try again. Returning None.")
            return None
        
        lower_strip(widget)

        if widget in self.widgets_with_text:
            log.info(f"{verifier_name(v)}: Verified! it's a widget with text.")
            widget = self.widgets_with_text[widget]()
            log.debug(f"{verifier_name(v)}: Returning: {class_name(widget)}")
            return widget
        elif widget in self.widgets_without_text:
            log.info(f"{verifier_name(v)}: Verified! it's a widget without text.")
            widget = self.widgets_without_text[widget]()
            log.debug(f"{verifier_name(v)}: Returning: {class_name(widget)}")
            return widget
        else:
            log.warning(f"{verifier_name('widget')}: invalid widget. Please try again. Returning None.")
            return None
        
    def layout_verifier(self, layout = None, child = None):
        v = "layout"
        log.info(f"{verifier_name(v)}: Entered value is ({layout} and its instance is ({class_name(layout)}))")

        if layout is None :
            log.warning(f"{verifier_name(v)}: Layout is None. Returning none")
            log.info(f"{verifier_name(v)}: TIP - Layouts allow children to be added.")
            return None
        elif layout == "":
            log.warning(f"{verifier_name(v)}: Layout initiated but left blank. Please try again. Returning None.")
            return None
        elif not isinstance(layout, str):
            log.warning(f"{verifier_name(v)}: Data type needs to be 'str'. Please try again. Returning None.")

        if child is None:
            log.warning(f"{verifier_name(v)}: Child is None.")
            return None

        lower_strip(layout)

        adders = []
        row_adder = lambda l: l.addRow(child)
        adders.append(row_adder)
        widget_adder = lambda l: l.addWidget(child)
        adders.append(widget_adder)

        if layout in self.layouts:
            log.info(f"{verifier_name(v)}: Verified!")
            layout = self.layouts[layout]()
            for adder in adders:
                try:
                    log.info(f"{verifier_name(v)}: attempting {adder}")
                    adder(layout)
                    log.debug(f"{verifier_name}: Success!")
                except Exception as e:
                    log.error(f"{verifier_name(v)}: Error - {e}")
            log.debug(f"{verifier_name(v)}: Returning: {class_name(layout)}") 
            return layout
        elif layout not in self.layouts:
            log.warning(f"{verifier_name(v)}: Invalid layout. Please try again. Returning None.")  
            return None  

    def alignement_verifier(self,widget = None, alignment = None):
        v = "alignment"
        log.info(f"{verifier_name(v)}: Entered value is ({alignment} and its instance is ({class_name(alignment)}))")

        if alignment is None:
            log.warning(f"{verifier_name(v)}: Alignment is None. Returning none")
            return None
        elif alignment == "":
            log.warning(f"{verifier_name(v)}: Alignment initiated but was left blank. Please try again.")
            return None
        
        if widget is None:
            return None

        alignment = lower_strip(alignment)

        if alignment in self.alignments:
            alignment = self.alignments[alignment]
            log.info(f"{verifier_name(v)}: Verified!")
            alignment_setter = lambda w,a: w.setAlignment(a)
            log.debug(f"{verifier_name(v)}: Returning {alignment_setter(widget, alignment)}")
            return alignment_setter(widget, alignment)

    def geometry_verifier(self,widget = None, geometry = None):
        v = "geometry"
        log.info(f"{verifier_name(v)}: Entered value is ({geometry}) and its instance is ({class_name(geometry)})")

        if geometry is None:
            log.info(f"{verifier_name(v)}: Geometry is None. Defaulting to PyQt geometry.")
            return None
        
        if widget is None:
            return None
        
        #TODO: expand to allow % sizing

        if not hasattr(geometry, "__iter__"):
            log.warning(f"{verifier_name(v)}: Geometry must be iterable (tuple or list). Returning None.")
            return None

        for integer in geometry:
            if isinstance(integer, int):
                log.info(f"{verifier_name(v)}: Confirmed! {integer} is an integer")
            else:
                log.warning(f"{verifier_name(v)}: Invalid Data type detected! {integer} is a {class_name(integer)}")
                return None

        if len(geometry) == 2:
            log.info(f"{verifier_name(v)}: Resize detected. Converting to '.resize'.")
            widget.resize(*geometry)        
        elif len(geometry) == 4:
            log.info(f"{verifier_name(v)}: Setting geometry.")
            widget.setGeometry(*geometry)
        else:
            log.warning(f"{verifier_name(v)}: Invalid input. Please make sure youre adding (x position, y position, Length, Width).")
            return None

    def object_name_verifier(self,widget = None, obj_name = None):
        v = "object name"
        log.info(f"{verifier_name(v)}: Entered value is ({obj_name}) and its instance is ({class_name(obj_name)})")

        if obj_name is None:
            log.info(f"{verifier_name(v)}: Object name is None. Defaulting to 'Enter Text Here'.")
            obj_name = "Enter Text Here"
            return obj_name
        elif obj_name == "":
            log.info(f"{verifier_name(v)}: Object name initiated but returned empty. Please enter text. Defaulting to 'Enter Text Here'.")
            obj_name = "Enter Text Here"
            return obj_name

        if widget is None:
            return None
        
        obj_name = strip(obj_name)
        
        if isinstance(obj_name, str):
            log.info(f"{verifier_name(v)}: Verified! Object Name is a string! Setting object name: '{obj_name}'")
            widget.setObjectName(obj_name)
        
        else:
            log.warning(f"{verifier_name(v)}: Invalid data type! Data type needs to be a string. Returning None.")
            return None

    def text_verifier(self,widget = None, text = None):
        v = "text"
        log.info(f"{verifier_name(v)}: Entered value is ({text}) and its instance is ({class_name(text)})")
        if widget is None:
            log.info(f"{verifier_name(v)}: widget is None. Please check widget verifier.")
            return None
        
        if text is None:
            log.info(f"{verifier_name(v)}: Text is None. Returning None.")
            return None
        
   
        if isinstance(text, str):
            log.info(f"{verifier_name(v)}: Verified! text is a string!")
            text = text.strip()
            if hasattr(widget, "setText"):
                if text == "":
                    log.info(f"{verifier_name(v)}: Text initiated but was left empty. Defaulting to 'Enter Text Here'")
                    text = "Enter Text Here"
                    widget.setText(text)            
            else:
                log.info(f"{verifier_name(v)}: Widget does not have attribute 'setText'.")
                return None

        # TODO: Allow for text edit via GUI
        # TODO: Make hasttr as a list and make it a for loop and widgets as a list too and run another for loop

    def title_verifier(self,widget = None, title = None):
        v = "text"
        log.info(f"{verifier_name(v)}: Entered value is ({title}) and its instance is ({class_name(title)})")
        if widget is None:
            log.info(f"{verifier_name(v)}: widget is None. Please check widget verifier.")
            return None
        
        if title is None:
            log.info(f"{verifier_name(v)}: Text is None. Returning None.")
            return None
        
   
        if isinstance(title, str):
            log.info(f"{verifier_name(v)}: Verified! Title is a string!")
            title = title.strip()
            if hasattr(widget, "setWindowTitle"):
                if title == "":
                    log.info(f"{verifier_name(v)}: Text initiated but was left empty. Defaulting to 'Enter Text Here'")
                    title = "Enter Text Here"
                    widget.setWindowTitle(title)            
            else:
                log.info(f"{verifier_name(v)}: Widget does not have attribute 'setWindowTitle'.")
                return None

    def child_verifier(self,layout = None, child = None):
        v = "child"
        log.info(f"{verifier_name(v)}: Entered value is ({child}) and its instance is ({class_name(child)})")

        if child is None:
            log.info(f"{verifier_name(v)}: Child is None. Returning None")
            return None
        
        if layout is None:
            log.warning(f"{verifier_name(v)}: Layout is None. Can't add a child if layout is None. Please try again.")
            return None
        
        layout_attrs = ["addRow", "addWidget", "addLayout", "addItem"]

        for attribute in layout_attrs:
            if hasattr(layout, attribute):
                adder = lambda l, a = attribute: getattr(l, a)(child)
                adder(layout)
                log.info(f"{verifier_name(v)}: Using {attribute} to add child.") 
                break   

    @divider_wrapper("=", 20)
    def widget_without_text_builder(self, widget = None,layout = None, alignment = None, title = None, geometry = None, child = None, obj_name = None, ):
        b = "widget without text"
        log.info(f"{builder_name(b)}: Initiating builder.")

        log.info(f"{builder_name(b)}: Botting verifiers")
        self.widget_verifier(widget)
        #should return a definition not a key.

        self.layout_verifier(layout, child)
        #should add layout (if any) to widget

        self.alignement_verifier(widget, alignment)
        #should add alignment (if any)

        self.title_verifier(widget, title)
        #should return a stripped title.

        self.geometry_verifier(widget, geometry)
        #should apply geometry or resize (if any).

        self.child_verifier(layout, child)
        #should apply child (if any).

        self.object_name_verifier(widget, obj_name)
        #should apply object name (recommended, if any).

        if isinstance(widget, QMainWindow):
            if hasattr(widget, "show"):
                log.info(f"{builder_name(b)}: Widget has attr: 'show'.")
                widget.show()
                return widget
            else:
                log.warning(f"{builder_name}: Main Window does not have attr 'show'. Please check log for corrective ation.")
        else:
            return widget

    @divider_wrapper("=", 20)
    def widget_with_text_builder(self, widget = None, text = None,layout = None, geometry = None, child = None, obj_name = None):
        b = "widget with text" 
        log.info(f"{builder_name(b)}: Initiating builder.")

        self.widget_verifier(widget)
        #Should return the definition not the key

        self.text_verifier(widget, text)
        #Should return a striped text.

        self.geometry_verifier(widget, geometry)
        #Should return either Geometry or Resize

        self.layout_verifier(layout)
        #Should retur the definition not the key.

        self.child_verifier(layout, child)
        #Should add the child accordingly.

        self.object_name_verifier(obj_name)
        #Should add the object name

        return widget


