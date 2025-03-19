from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView,QLabel,QApplication, QMainWindow
from PyQt5.QtGui import QWindow
from MainLoginDialog import MainLoginDialog
from StaffLogin import StaffLogin

class MainWindow(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.ui = uic.loadUi('Mainwindow.ui')
        self.ui.show()
        
        # MainLogin dialog.
        self.main_login_dialog = MainLoginDialog()
        
        
        # Sales dialog.
        self.staff_dialog = StaffLogin()
        
        
        self.ui.custButton.clicked.connect(self.show_main_login_dialog)
        self.ui.staffButton.clicked.connect(self._show_staff_dialog)
        #self.ui.set_background_image(r"C:\Users\pmgan\data225\Main_Project_12_03\Main_Project\Image.jpg")
        
    #def set_background_image(self, image_path):
        # Create a QLabel to hold the background image
        #background_label = QLabel(self)
        #background_label.setGeometry(0, 0, self.width(), self.height())

        # Load the image and set it as the pixmap for the label
        #pixmap = QPixmap(image_path)
        #background_label.setPixmap(pixmap)
        #background_label.setScaledContents(True)
            
            

    def show_main_login_dialog(self):
        """
        Show the car dialog.
        """
        self.main_login_dialog.show_dialog()
        #self.ui.close()

    def _show_staff_dialog(self):
        """
        Show the sales dialog.
        """
        self.staff_dialog.show_dialog()
        #self.ui.close()
