### Libraries
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QGridLayout, QLineEdit, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QIcon
import urllib.request
from coffeelog import BaseLogger
import sys
from decouple import config

### Local
from helpers import clear_layout, validate_roomcode, get_dummy_room, copy_to_clipboard, get_image_url
from room import Room

class Client(QMainWindow):
    
    ### Init methods
    
    def __init__(self, api_handler) -> None:
        self.logger = BaseLogger(type(self).__name__)  
        
        self.app = QApplication(sys.argv)
        self.api_handler = api_handler
        self.roomstate = None
        super().__init__()
        
        self.workers = []
        self.progress_timer = QTimer(self)
        self.album_cover_container = None
        
        
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
        
        playback_bar = QProgressBar(self)
        # Global CSS as no other progress bar will ever be needed
        playback_bar.setStyleSheet('QProgressBar {min-height: 12px;max-height: 12px;border-radius: 6px;}')
        playback_bar.setTextVisible(False)
        current_playback = self.api_handler.get_playback()
        playback_bar.setMaximum(current_playback['item']['duration_ms']/1000)
        self.progress_timer.timeout.connect(lambda: self.advance_playback_bar(playback_bar))
        self.progress_timer.setInterval(1000)
        if self.api_handler.is_playing:
            self.progress_timer.start()
        playback_bar.setValue(current_playback['progress_ms']/1000)
        
        
        cover_dimension = int(config('ALBUM_COVER_SIZE'))
        data = urllib.request.urlopen(get_image_url(current_playback['item']['album']['images'],cover_dimension)).read()
        loaded_image = QPixmap()
        loaded_image.loadFromData(data)
        
        self.album_cover_container = QLabel(self)
        self.album_cover_container.setPixmap(loaded_image)
        self.album_cover_container.setGeometry(cover_dimension, cover_dimension, cover_dimension, cover_dimension)
        
       
        self.centralWidget().layout().addWidget(copy_roomcode_button, 0, 0)
        self.centralWidget().layout().addWidget(leave_button, 0, 2)
        self.centralWidget().layout().addWidget(pausePlay_button, 3, 0)
        self.centralWidget().layout().addWidget(playback_bar, 3, 1, 1, 2)
        self.centralWidget().layout().addWidget(self.album_cover_container, 2, 1)
           
        
    ### Helper Methods
    def advance_playback_bar(self, bar) -> None:
        bar.setValue(bar.value() + 1)
        # On song finish
        if bar.value() == bar.maximum():
            self.update_cover_image()
            bar.setValue(0)  
            
    def update_cover_image(self):
        if not self.album_cover_container:
            pass
        
        
         
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
        self.album_cover_container = None
        self.api_handler.change_playback_state(False)
        self.logger.debug('Left room')
        
        # Stop running workers
        self.progress_timer.stop()
        for worker in self.workers:
            worker.stop()
        self.workers = []
        
        self.init_start_ui()
            
            
    def btn_playback_toggle(self, button) -> None:
        self.logger.debug('Setting playback state')
        is_playing = self.api_handler.change_playback_state()
        if is_playing is True:
            button.setText('Pause')
            if not self.progress_timer.isActive():
                self.progress_timer.start()
        else:
            button.setText('Play')
            if self.progress_timer.isActive():
                self.progress_timer.stop()
            
            
    def copy_roomcode(self) -> None:
        self.logger.debug('Copying roomcode')
        print(self.roomstate.roomcode)
        copy_to_clipboard(self.roomstate.roomcode)
            
        
        
        
    
    
        