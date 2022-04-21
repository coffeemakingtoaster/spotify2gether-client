class Room:
    
    def __init__(self, name=None, description=None, roomcode=None, current_song=None, current_offset=0) -> None:
        self.name = name
        self.description = description
        self.roomcode = roomcode
        self.current_song = current_song
        self.current_offset = current_offset
        self.users = []
        self.queue = []
    
    def parse_remote_metadata(self, data) -> None:
        pass