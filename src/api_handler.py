# Libraries
import spotipy
from spotipy.oauth2 import SpotifyPKCE
from decouple import config
from coffeelog import BaseLogger
from typing import Dict

# Local
from helpers import generate_random_string
from room import Room

class ApiHandler():
    def __init__(self) -> None:
        self.logger = BaseLogger(type(self).__name__)  
        self.user = None
        self.is_playing = True
        self.device = None
        
    
    def start_auth_flow(self):
        self.logger.debug("Instancitaing spotipy")
        # Generate Auth manager with PCKE as the server is not supposed to interact with the spotify API
        auth_manager = SpotifyPKCE(client_id=config("CLIENT_ID"), scope=config("AUTH_SCOPE"), state=generate_random_string(16), redirect_uri=config("AUTH_REDIRECT_URI") )
        self.spotipy = spotipy.Spotify(client_credentials_manager=auth_manager)
        self.logger.debug("Successfully authorized account")
        self.user = self.spotipy.me()
        self.logger.debug(f'User: {self.user}')
        
    
    def refresh_devices(self):
        self.logger.debug(f'Getting devices')
        # Get all devices and set to default
        devices = self.spotipy.devices()
        if len(devices) == 0:
            self.logger.error("No devices found for this user")
        
        
    def change_playback_state(self, forced_playback_state = None) -> bool:
        # Force Playback State
        if forced_playback_state is not None:
            self.logger.debug(f'Playback state forced to {forced_playback_state}')
            self.is_playing = not forced_playback_state  
        if self.is_playing == True:
            self.spotipy.pause_playback()
        else:
            self.spotipy.start_playback()
        self.is_playing = not self.is_playing
        self.logger.debug(f'Playback state changed to {self.is_playing}')
        return self.is_playing
    
    
    def get_playback(self):
        playback = self.spotipy.currently_playing()
        if not playback:
            self.logger.error('Cannot get playback. This might be due to spotify being in a private session')
        self.is_playing = playback['is_playing']
        return playback
    
    
    def prepare_for_room(self, room: Room) -> None:
        self.spotipy.start_playback(device_id=self.device, uris=[room.current_song], position_ms=room.current_offset)
        pass
    
    def skip_song(self, track) -> None:
        self.spotipy.start_playback(device_id=self.device, uris=[track], position_ms=0)
        
    def get_song_info(self, track) -> Dict:
        print(self.spotipy.track(track))
        return self.spotipy.track(track)