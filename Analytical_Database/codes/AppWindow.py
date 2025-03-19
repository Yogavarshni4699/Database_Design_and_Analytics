from PyQt5.QtGui import QWindow

from LandingWindow import LandingWindow

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
        self._student_dialog = LandingWindow()
        self._student_dialog.show_dialog()
        #self.ui.student_button.clicked.connect(self._show_car_dialog)
        
     
