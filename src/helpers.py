from random import SystemRandom
from string import ascii_letters, digits
from PyQt6.QtWidgets import QLabel

def generate_random_string(length: int) -> str:
    return ''.join(SystemRandom().choice(ascii_letters + digits) for _ in range(length))

def clear_layout(layout) -> None:
    while layout.count():
        print('clearing')
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        