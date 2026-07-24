class PodcastManager:
    def __init__(self):
        self.subscriptions = []
        self.episodes_listened = []

    def subscribe_podcast(self, podcast_name, channel):
        """Subscribe to a podcast."""
        self.subscriptions.append({
            'name': podcast_name,
            'channel': channel,
            'subscribed_date': None
        })

    def add_to_queue(self, episode_title, podcast_name):
        """Add episode to listening queue."""
        return {'episode': episode_title, 'podcast': podcast_name, 'queued': True}

    def mark_listened(self, episode_id, duration_listened=None):
        """Mark an episode as listened."""
        self.episodes_listened.append({
            'episode_id': episode_id,
            'duration_listened': duration_listened,
            'completed': True
        })

    def get_recommendations(self):
        """Get podcast recommendations."""
        return {'recommendations': [], 'based_on': 'listening_history'}
