import sys
from PyQt5 import uic
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QMainWindow
from DATA225utils import make_connection
from TitanicWindowCustomer import TitanicWindowCustomer
from PyQt5.QtCore import QThread , pyqtSignal, QObject
import time

class WorkerThread(QThread):
    # Define a signal
    call_main_thread_method = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = False 
        self.changed_key = ""
        self.order_status_dict = {}
    def start_t(self):
        self.running = True
        self.start()
    def get_changed_key(self):
        return self.changed_key
    def update_dict(self, dictn):
        self.order_status_dict = dictn
    def is_status_changed(self, order_id):
        conn = make_connection(config_file = 'techorcas_db.ini')
        cursor = conn.cursor()
        status = ""
        sql = ("""
                select is_status_changed from orders_table where
            """
            f"orders_table.OrderID = '{order_id}' "
            )
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in rows:
            status = row[0]
        
        return status
        
    def clear_status_set(self, order_id):
        conn = make_connection(config_file = 'techorcas_db.ini')
        cursor = conn.cursor()
        status = ""
        sql = ("""
                UPDATE orders_table
               """
                f"SET orders_table.is_status_changed = false WHERE orders_table.OrderID = '{order_id}'"
              )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()

        
        cursor.close()
        conn.close()

    def get_status(self, order_id):
        conn = make_connection(config_file = 'techorcas_db.ini')
        cursor = conn.cursor()
        status = ""
        sql = ("""
                select Status from orders_table where
            """
            f"orders_table.OrderID = '{order_id}' "
            )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        cursor.close()
        conn.close()

        for row in rows:
            status = row[0]
        
        return status
    def stop(self):
        self.running = False
    def run(self):
        # Your polling logic here
        while self.running:
            for key in self.order_status_dict:
                trigger = self.is_status_changed(key);
                print (trigger)
                curr_status = self.get_status(key)
                old_status = self.order_status_dict[key]
                if trigger :
                    self.call_main_thread_method.emit()
                    self.changed_key = key
                    self.order_status_dict[key] = curr_status
                    self.clear_status_set(key)

            print(f"Polled at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            # Wait for the specified interval before polling again
            time.sleep(5)
        print(f"Polling finished at {time.strftime('%Y-%m-%d %H:%M:%S')}")

class OrderStatus(QDialog):
    '''
    The student dialog
    '''
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        self.worker_thread = WorkerThread()

        # Load the dialog components.
        self.ui = uic.loadUi('Status.ui')
        self.notif_ui = uic.loadUi('OrderNotif.ui')
        
        self.email = ""
        self.date_dict = {}
        self.order_status_dict = {}
        
        self.ui.checkStatusButton.clicked.connect(self.show_status)
        self.ui.analysisButton.clicked.connect(self.show_analysis)
        self.ui.feedbackSubmitButton.clicked.connect(self.submit_feedbaack)
        self.ui.dateCombo.currentIndexChanged.connect(self.update_order_list)
        
        #Notif dialog
        #self.notif_ui.ViewNotifButton.clicked.connect(self.notif_view)
        #self.notif_ui.IgnoreNotifButton.clicked.connect(self.notif_ignore)
        self.statusPollerThread = False
        #self.ui.horizontalSlider.valueChanged.connect()
        #self.ui.orderIdCombo.currentIndexChanged.connect(self._enter_sales_count)
    def closeEvent(self, event):
        self.worker_thread.stop()
        self.worker_thread.wait()  # Wait for the thread to finish
        super().closeEvent(event)

        
    def status_callback(self):
        order_id = self.worker_thread.get_changed_key()
        exists = False
        for key, value in self.date_dict.items():
            for val in value:
                if val == order_id:
                    exists = True
        if exists:
            self.notif_ui.NotifOrderIdDisplay.setText(order_id)
            self.notif_ui.NotifStatusDisplay.setText(self.get_status(order_id))
            self.notif_ui.show()
        else :
            print("Order ID match not found, ord_id: " , order_id)
    
    def notif_view(self):
        ord_id = self.notif_ui.NotifOrderIdDisplay.text()
        date = ""
        exists = False
        for key, val in self.date_dict.items():
            for value in val:
                if value == ord_id:
                    exists = True
                    date = key
        if exists:
            self.ui.dateCombo.setCurrentText(date)
            self.ui.orderIdCombo.setCurrentText(ord_id)
            self.show_status()
        else :
            print("Order ID match error, not expected, ord_id: " , ord_id)

    def  notif_ignore(self):
        self.notif_ui.close()
    
    def show_analysis(self):
        self.analysis_obj.show_dialog()
        
    def show_status(self):
        """
        Displays statusText
        """
        curr_order = self.ui.orderIdCombo.currentText()
        ord_status = self.get_status(curr_order)
        self.ui.statusTextField.setText(ord_status)
        self.ui.commentsTextFiled.clear()
        self.ui.ratingDial.setValue(0) 
    
    def get_status(self, order_id):
        conn = make_connection(config_file = 'techorcas_db.ini')
        cursor = conn.cursor()
        status = ""
        sql = ("""
                select Status from orders_table where
            """
            f"orders_table.OrderID = '{order_id}' "
            )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        cursor.close()
        conn.close()

        # Set the menu items to the students' names.
        for row in rows:
            status = row[0]
        
        return status
    def submit_feedbaack(self):
        """
        Submits feedback to DB
        """
        curr_order = self.ui.orderIdCombo.currentText()
        curr_dial = self.ui.ratingDial.value()
        curr_feedback = self.ui.commentsTextFiled.toPlainText()
        print("Order, dial, comm : ", curr_order, curr_dial, curr_feedback)
        conn = make_connection(config_file = 'techorcas_db.ini')
        cursor = conn.cursor()
        
        
        sql = ("""
                UPDATE customers_table
               """
                f"SET customers_table.Rating = '{curr_dial}', customers_table.Feedback = '{curr_feedback}' WHERE customers_table.OrderID = '{curr_order}'"
              )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
            
        cursor.close()
        conn.close()
        self.ui.commentsTextFiled.clear()
        self.ui.ratingDial.setValue(0)   

        
    
    def set_dateCombo(self, email):
        """
        Updates dates in datecombo based on user
        """
        
        # Set the menu items to the students' names.
        for date_op in self.date_dict.keys():
            self.ui.dateCombo.addItem(date_op)
        
    def update_order_list(self):
        """
        Updates orders based on date selected
        """
        self.ui.orderIdCombo.clear()
        curr_date = self.ui.dateCombo.currentText()
        print("Curr_date:", curr_date)
        
        for lst in self.date_dict[curr_date]:
            print("Inserting LST: ", lst)
            self.ui.orderIdCombo.addItem(lst)
        
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
        self.statusPollerThread = True;
        #self.status_poller(20)
    
    
    def show_exist_user_dialog(self):
        """
        Show the sales dialog.
        """
        self.existingUser.show_dialog() #Show thanks for submitting UI

    def _initialize_table(self):
        """
        Initialize OrderID, status, feedback, comments section.
        
        self.ui.sales_list_table.clear()
        """
        self.ui.orderIdCombo.clear()
        self.ui.statusTextField.clear()
        self.ui.feedbackCombo.clear()
        self.ui.commentsTextFiled.clear()
    
    def fetch_all_data(self, email):
    
        self.email = email
        self.analysis_obj = TitanicWindowCustomer(email)

        self.date_dict.clear()
        
        conn = make_connection(config_file = 'techorcas_db.ini')
        cursor = conn.cursor()
        
        sql = ("""
                select distinct orders_table.Date from orders_table,customers_table
                where orders_table.OrderID = customers_table.OrderID and 
            """
            f"customers_table.Email = '{email}' "
            )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        for row in rows:
            date_op = row[0]
            self.date_dict.setdefault(date_op,[])
            
        
        sql = ("""
                select distinct customers_table.OrderID from customers_table 
                where
            """
            
            f"customers_table.Email = '{self.email}' "
            )
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        for row in rows:
            ord_id = row[0]
            sql = ("""
                select distinct orders_table.Date from orders_table 
                where
            """
            
            f"orders_table.OrderID = '{ord_id}' "
            )
        
            cursor.execute(sql)
            op = cursor.fetchall()
            self.date_dict.setdefault(op[0][0],[]).append(ord_id)
        
        for key in self.date_dict:
            ord_list = self.date_dict[key]
            for value in ord_list:
                ord_status = self.get_status(value)
                self.order_status_dict.update({value:ord_status})
                print("First status:", value, ord_status)
                
        
    def status_poller(self, interval):
        self.worker_thread.update_dict(self.order_status_dict)
        self.worker_thread.call_main_thread_method.connect(self.status_callback)
        
        self.worker_thread.start_t()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = OrderStatus()
    form.show_dialog()
    sys.exit(app.exec_())        