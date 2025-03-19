import sys
from PyQt5 import uic
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView
from DATA225utils import make_connection
from OrderStatus import OrderStatus

class StatusUpdate(QWindow):
    '''
    The student dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('status_update.ui')
        
        self.staffEmail = "";
        self.statusChoices = ['Shipped', 'Cancelled', 'Pending', 'Pending - Waiting for Pick Up', 'Shipped - Delivered to Buyer',
                                'Shipped - Returned to Seller', 'Shipped - Picked Up', 'Shipped - Returning to Seller', 
                                 'Shipped - Out for Delivery', 'Shipped - Rejected by Buyer', 'Shipped - Damaged', 'Shipping' ]
        
        self.ui.updateButton.clicked.connect(self.submit_feedbaack)
    
   
    def submit_feedbaack(self):
        """
        Submits feedback to DB
        """
        curr_order = self.ui.OrderCombo.currentText()
        curr_status = self.ui.StatusCombo.currentText()
        print("Order, Status : ", curr_order, curr_status)
        conn = make_connection(config_file = 'techorcas_db.ini')
        cursor = conn.cursor()
        
        
        sql = ("""
                UPDATE orders_table
               """
                f"SET orders_table.Status = '{curr_status}', orders_table.is_status_changed = true WHERE orders_table.OrderID = '{curr_order}'"
              )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
            
        cursor.close()
        conn.close()
        
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()       
    
    def fetch_all_data(self, email):
    
        self.staffEmail = email
        
        conn = make_connection(config_file = 'techorcas_db.ini')
        cursor = conn.cursor()
        
        sql = ("""
                select StaffID from Staff_table where
            """
            f"Staff_table.Staff_Email = '{email}' "
            )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        staffId = rows[0][0]
        print("Staff ID: ", staffId)
            
        
        sql = ("""
                select OrderID from orders_table 
                where
            """
            
            f"orders_table.StaffID = '{staffId}' "
            )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        for row in rows:
            ord_id = row[0]
            self.ui.OrderCombo.addItem(ord_id)
        for tmp in self.statusChoices:
            self.ui.StatusCombo.addItem(tmp)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = StatusUpdate()
    form.show_dialog()
    sys.exit(app.exec_())        