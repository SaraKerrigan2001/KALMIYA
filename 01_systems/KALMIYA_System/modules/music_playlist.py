class MusicPlaylistGenerator:
    def __init__(self):
        self.playlists = {}
        self.listening_history = []

    def create_playlist(self, playlist_name, mood=None, genre=None):
        """Create a new playlist."""
        self.playlists[playlist_name] = {
            'mood': mood,
            'genre': genre,
            'tracks': [],
            'created_date': None
        }

    def add_track(self, playlist_name, track_name, artist):
        """Add a track to a playlist."""
        if playlist_name in self.playlists:
            self.playlists[playlist_name]['tracks'].append({
                'name': track_name,
                'artist': artist
            })

    def generate_mood_playlist(self, mood, duration=30):
        """Generate a playlist based on mood."""
        return {'mood': mood, 'duration_minutes': duration, 'tracks': []}

    def get_listening_history(self):
        """Get user listening history."""
        return self.listening_history
