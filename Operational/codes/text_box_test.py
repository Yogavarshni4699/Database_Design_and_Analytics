import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create a QLineEdit widget
        self.password_edit = QLineEdit(self)
        
        # Set the echo mode to Password to mask the entered characters
        self.password_edit.setEchoMode(QLineEdit.Password)

        # Create a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.password_edit)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget
        self.setCentralWidget(central_widget)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('QLineEdit as Password Box Example')
        self.show()

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
