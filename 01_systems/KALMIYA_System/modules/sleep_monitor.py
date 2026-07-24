class SleepMonitor:
    def __init__(self):
        self.sleep_logs = []

    def log_sleep(self, bedtime, wake_time, quality_rating=None):
        """Log a sleep session."""
        self.sleep_logs.append({
            'bedtime': bedtime,
            'wake_time': wake_time,
            'quality': quality_rating,
            'duration': None
        })

    def analyze_sleep_patterns(self):
        """Analyze sleep patterns and trends."""
        return {
            'total_nights': len(self.sleep_logs),
            'average_duration': None,
            'patterns': []
        }

    def get_sleep_recommendation(self):
        """Get personalized sleep recommendations."""
        return {'recommendation': 'Maintain consistent sleep schedule'}
