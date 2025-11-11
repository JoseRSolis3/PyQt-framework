from log_util import advanced_log
from dictionaries.sanity_checker.verifiers import application, stacked, page
from PyQt6.QtWidgets import QApplication
import sys
    
class App():
    def __init__(self):
        initialize = QApplication(sys.argv)
        self.stack = stacked(self.pages())
        self.app = application(self.stack, None)
        sys.exit(initialize.exec())
    
    def pages(self):
        page_list = []
        self.main_page = Login().parent_w()
        page_list.append(self.main_page)
        return page_list

class Login():
    def __init__(self) -> None:
        pass

    def parent_w(self):
        self.pg = page((500,300), None, "login")
        return self.pg

if __name__ == "__main__":
    app = App()