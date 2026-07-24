class GamingMode:
    def __init__(self):
        self.games = []
        self.playtime_log = []
        self.is_active = False

    def activate_gaming_mode(self):
        """Activate gaming mode (minimize distractions)."""
        self.is_active = True
        return {'status': 'active', 'distractions_minimized': True}

    def deactivate_gaming_mode(self):
        """Deactivate gaming mode."""
        self.is_active = False
        return {'status': 'inactive'}

    def add_game(self, game_name, platform):
        """Add a game to library."""
        self.games.append({
            'name': game_name,
            'platform': platform,
            'playtime': 0
        })

    def log_playtime(self, game_name, duration):
        """Log gaming session."""
        self.playtime_log.append({
            'game': game_name,
            'duration': duration,
            'timestamp': None
        })

    def get_stats(self):
        """Get gaming statistics."""
        return {'games': len(self.games), 'total_playtime': sum(p['duration'] for p in self.playtime_log)}
