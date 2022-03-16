### Libraries
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QGridLayout, QLineEdit, QLabel
from PyQt6.QtCore import Qt
from coffeelog import BaseLogger
import sys

### Local
from helpers import clear_layout, validate_roomcode, get_dummy_room, copy_to_clipboard
from room import Room

class Client(QMainWindow):
    
    ### Init methods
    
    def __init__(self, api_handler) -> None:
        self.logger = BaseLogger(type(self).__name__)  
        
        self.app = QApplication(sys.argv)
        self.api_handler = api_handler
        self.roomstate = None
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
        # Prepare Layout
        clear_layout(self.centralWidget().layout())
        self.centralWidget().layout().setRowStretch(0, 0)
        
        roomcode_input = QLineEdit(self)
        join_button = QPushButton('Join', self)
        join_button.clicked.connect(lambda: self.btn_join_room(roomcode_input))
        create_button = QPushButton('Create', self)
        create_button.clicked.connect(self.btn_create_room)
        # Empty label for error messages
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet('QLabel {color: red;}') 
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.centralWidget().layout().addWidget(self.error_label, 0, 0, 1, 2)
        self.centralWidget().layout().addWidget(roomcode_input, 1, 0, 1, 2)
        self.centralWidget().layout().addWidget(join_button, 2, 0)
        self.centralWidget().layout().addWidget(create_button, 2, 1)
        
        
    def init_room_ui(self, room: Room) -> None:
        self.roomstate = room
        
        # Prepare Layout
        clear_layout(self.centralWidget().layout())
        self.centralWidget().layout().setRowStretch(0, 0)
        
        self.setWindowTitle(room.name)
        pausePlay_button = QPushButton('Pause', self)
        pausePlay_button.clicked.connect(lambda: self.btn_playback_toggle(pausePlay_button))
        leave_button = QPushButton('Leave', self)
        leave_button.clicked.connect(self.btn_leave_room)
        copy_roomcode_button = QPushButton('Copy Roomcode', self)
        copy_roomcode_button.clicked.connect(self.copy_roomcode)
        
        self.centralWidget().layout().addWidget(copy_roomcode_button, 0, 2)
        self.centralWidget().layout().addWidget(leave_button, 0, 2)
        self.centralWidget().layout().addWidget(pausePlay_button, 1, 0)
        
        
        
        
        
        
         
    ### Button Methods
    def btn_init_auth(self) -> None:
        self.api_handler.start_auth_flow()
        self.init_start_ui()
            
    def btn_join_room(self, roomcode_input) -> None:
        if not roomcode_input:
            return
        if not validate_roomcode(roomcode_input.text()):
            self.error_label.setText('Invalid room code')
            self.logger.debug(f'Join with invalid code')
            return
        self.error_label.setText('Could not join room')
        self.logger.error(f'Could not join room')
    
    def btn_create_room(self) -> None:
        try:
            self.init_room_ui(get_dummy_room())
        except Exception() as e:
            self.error_label.setText('Could not create room')
            self.logger.error(f'Could not create room: {e}')
        self.logger.debug('Joined Room')
            
    def btn_leave_room(self) -> None:
        self.logger.debug('Leaving room')
        self.roomstate = None
        self.api_handler.change_playback_state(False)
        self.logger.debug('Left room')
        self.init_start_ui()
            
            
    def btn_playback_toggle(self, button) -> None:
        self.logger.debug('Setting playback state')
        state = self.api_handler.change_playback_state()
        if state is True:
            button.setText('Pause')
        else:
            button.setText('Play')
            
            
    def copy_roomcode(self) -> None:
        self.logger.debug('Copying roomcode')
        print(self.roomstate.roomcode)
        copy_to_clipboard(self.roomstate.roomcode)
            
        
        
        
    
    
        