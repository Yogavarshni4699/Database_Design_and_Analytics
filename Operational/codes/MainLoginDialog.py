import sys
from PyQt5 import uic
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView
from ExistUserLogin import ExistUserLogin
from NewUserReg import NewUserReg

class MainLoginDialog(QWindow):
    '''
    The student dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('MainLogin.ui')
        
        self.existingUser = ExistUserLogin()
        self.newUser = NewUserReg()


        self.ui.newAccountButton.clicked.connect(self.show_new_user_dialog)
        self.ui.existAccountButton.clicked.connect(self.show_exist_user_dialog)        
    
    
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    
    def show_new_user_dialog(self):
        """
        Show the car dialog.
        """
        self.newUser.show_dialog()
        #self.ui.close()


    def show_exist_user_dialog(self):
        """
        Show the sales dialog.
        """
        self.existingUser.show_dialog() 
        #self.ui.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainLoginDialog()
    form.show_dialog()
    sys.exit(app.exec_())        