import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView
from DATA225utils import make_connection
from PyQt5.QtCore import QTimer

class NewUserReg(QDialog):
    '''
    The student dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('new_login.ui')

        
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        form = NewUserReg()
        form.show_dialog()
        sys.exit(app.exec_()) 
    
    