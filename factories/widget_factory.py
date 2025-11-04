from PyQt6.QtWidgets import (
    QApplication,QMainWindow, QWidget, QStackedWidget,
    QPushButton, QLabel, QLineEdit, QComboBox,
    QVBoxLayout, QHBoxLayout, QFormLayout
)

from PyQt6.QtCore import Qt

from log_util import advanced_log

import inspect
import sys
import os

advanced_log("info", "TEST LOG")

class_name = lambda w: w.__class__.__name__
reminder = "|**REMINDER**|:"
default_text = "Enter Text Here"

