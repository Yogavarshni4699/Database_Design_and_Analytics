import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QLineEdit
from DATA225utils import make_connection
from PyQt5.QtCore import QTimer
from argon2 import PasswordHasher
from OrderStatus import OrderStatus
import time
import threading

class ExistUserLogin(QDialog):
    '''
    The student dialog
    '''

    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('login.ui')
        
        self.order_status = OrderStatus()

        # Student menu and query button event handlers.
        self.ui.loginButton.clicked.connect(self.VerifyLogin)
        
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    def VerifyLogin(self):
        """
        Initialize the student menu with student names from the database.
        """
        
        email_inp = self.ui.emailInput.text()
        pass_inp = self.ui.passInput.text()
        
        
        conn = make_connection(config_file = 'techorcas_db.ini')
        cursor = conn.cursor()
        
        sql = ("""
            SELECT Password FROM customers_table 
            """
            f"where Email = '{email_inp}' "
            )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        cursor.close()
        conn.close()
         
        is_password_correct = False
   
        #db_pw = output hash from db
        if len(rows) > 0: 
            db_pw = rows[0][0]  # Assuming Password is in the first column

            print("Email: ", email_inp)
            print("Pass: ", pass_inp)
            hasher = PasswordHasher()
            print("Hashed Password:", db_pw)
            try:
                # Code that may raise an exception
                is_password_correct = hasher.verify(db_pw, pass_inp)
                print("This line will not be executed if an exception occurs.")
            except Exception as e:
                # Code to handle the exception
                print(f"An error occurred: {e}")
            else:
                # Code that will be executed if no exception occurs
                print("No exception occurred.")
            finally:
                # Code that will be executed no matter what, whether an exception occurred or not
                print("Is Password Correct?", is_password_correct)
        else :
            print("Unable to find user with email: ", email_inp)
            
            
        
        if is_password_correct:
            self.order_status.fetch_all_data(email_inp)
            self.order_status.show_dialog()
            self.order_status.set_dateCombo(email_inp)
            self.ui.close()
            polling_interval = 20
            poller_thread = threading.Thread(target=self.order_status.status_poller, args=(polling_interval,))
            poller_thread.start()
     
            
    def _adjust_column_widths(self):
        """
        Adjust the column widths of the class table to fit the contents.
        """
        header = self.ui.sales_list_table.horizontalHeader();
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)  

    def Show_status_order_dialogbox(self):
        """
        Show the status and feedback dialog.
        """
        #self.order_status.show_dialog()   
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ExistUserLogin()
    form.show_dialog()
    sys.exit(app.exec_())        