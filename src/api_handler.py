# Libraries
import spotipy
from spotipy.oauth2 import SpotifyPKCE
from decouple import config
from coffeelog import BaseLogger

# Local
from helpers import generate_random_string

class ApiHandler():
    def __init__(self) -> None:
        self.logger = BaseLogger(type(self).__name__)  
        self.user = None
    
    def start_auth_flow(self):
        self.logger.debug("Instancitaing spotipy")
        # Generate Auth manager with PCKE as the server is not supposed to interact with the spotify API
        auth_manager = SpotifyPKCE(client_id=config("CLIENT_ID"), scope=config("AUTH_SCOPE"), state=generate_random_string(16), redirect_uri=config("AUTH_REDIRECT_URI") )
        self.spotipy = spotipy.Spotify(client_credentials_manager=auth_manager)
        self.logger.debug("Successfully authorized account")