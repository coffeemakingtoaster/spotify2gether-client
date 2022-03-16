# Libraries
from random import SystemRandom
from string import ascii_letters, digits
from PyQt6.QtWidgets import QLabel
from pyperclip import copy

# Local
from room import Room

def generate_random_string(length: int) -> str:
    return ''.join(SystemRandom().choice(ascii_letters + digits) for _ in range(length))

def clear_layout(layout) -> None:
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        
def validate_roomcode(code: str) -> bool:
    # length
    if len(code) != 8 :
        return False
    
    if not code.isalnum():
        return False
    
    return True


        
def get_dummy_room() -> Room:
    room = Room(name='Dummy Room', description='Dummy Room Description', roomcode='000DUMMY')
    print(room.roomcode)
    return room
    
    
def copy_to_clipboard(value: str) -> None:
    copy(value)
    