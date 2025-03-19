from PyQt5.QtGui import QWindow

from TitanicWindowCustomer import TitanicWindowCustomer

class AppWindow(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()

        # Student dialog.
        self._student_dialog = TitanicWindowCustomer()
        self._student_dialog.show_dialog()
        #self.ui.student_button.clicked.connect(self._show_car_dialog)
        
     
