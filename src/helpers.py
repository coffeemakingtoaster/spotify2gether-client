from random import SystemRandom
from string import ascii_letters, digits

def generate_random_string(length):
    return ''.join(SystemRandom().choice(ascii_letters + digits) for _ in range(length))