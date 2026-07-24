class ConferenceMode:
    def __init__(self):
        self.active_conference = None
        self.participants = []
        self.notes = []

    def start_conference(self, conference_name, duration=None):
        """Start a conference session."""
        self.active_conference = {
            'name': conference_name,
            'duration': duration,
            'start_time': None,
            'participants': self.participants
        }
        return self.active_conference

    def add_participant(self, name, email=None):
        """Add conference participant."""
        self.participants.append({
            'name': name,
            'email': email,
            'joined_time': None
        })

    def take_note(self, note_text, timestamp=None):
        """Take a conference note."""
        self.notes.append({
            'text': note_text,
            'timestamp': timestamp
        })

    def enable_recording(self):
        """Enable conference recording."""
        return {'recording': True}

    def end_conference(self):
        """End conference session."""
        self.active_conference = None
        return {'conference_ended': True}

    def generate_summary(self):
        """Generate conference summary."""
        return {'participants': len(self.participants), 'notes': len(self.notes)}
