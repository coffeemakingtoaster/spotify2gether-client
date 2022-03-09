### Libraries
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QGridLayout, QLineEdit, QLabel
from PyQt6.QtCore import pyqtSlot
from coffeelog import BaseLogger
import sys

### Local
from helpers import clear_layout

class Client(QMainWindow):
    
    ### Init methods
    
    def __init__(self, api_handler) -> None:
        self.logger = BaseLogger(type(self).__name__)  
        
        self.app = QApplication(sys.argv)
        self.api_handler = api_handler
        super().__init__()
        
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QGridLayout())
        self.init_window()
        

    def init_window(self) -> None:
        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('Client')
        self.init_login_ui()
        self.error_label = None
        self.show()
        self.logger.debug('Client started')
        
    def start(self):
        self.app.exec()
        
    
    ### UI Methods
        
    def init_login_ui(self) -> None:
        clear_layout(self.centralWidget().layout())
        button = QPushButton('Login', self)
        button.clicked.connect(self.btn_init_auth)
        self.centralWidget().layout().addWidget(button)
            
    
    
    def init_start_ui(self) -> None:
        clear_layout(self.centralWidget().layout())
        roomcode_input = QLineEdit(self)
        join_button = QPushButton('Join', self)
        join_button.clicked.connect(self.btn_join_room)
        create_button = QPushButton('Create', self)
        create_button.clicked.connect(self.btn_create_room)
        # Empty label for error messages
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet('QLabel {color: red;}') 
        self.centralWidget().layout().addWidget(self.error_label, 0, 0, 1, 2)
        self.centralWidget().layout().addWidget(roomcode_input, 1, 0, 1, 2)
        self.centralWidget().layout().addWidget(join_button, 2, 0)
        self.centralWidget().layout().addWidget(create_button, 2, 1)
        
         
    ### Button Methods
    def btn_init_auth(self) -> None:
        self.api_handler.start_auth_flow()
        self.init_start_ui()
            
    def btn_join_room(self) -> None:
        self.error_label.setText('Could not join room')
    
    def btn_create_room(self) -> None:
        self.error_label.setText('Could not create room')
        
        
    
    
        