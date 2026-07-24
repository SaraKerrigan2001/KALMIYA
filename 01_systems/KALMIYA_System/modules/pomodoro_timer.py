class PomodoroTimer:
    def __init__(self, work_duration=25, break_duration=5):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.sessions = []
        self.current_session = None

    def start_session(self, task_name):
        """Start a new Pomodoro work session."""
        self.current_session = {
            'task': task_name,
            'start_time': None,
            'end_time': None,
            'duration': self.work_duration
        }

    def complete_session(self):
        """Complete current session and log it."""
        if self.current_session:
            self.sessions.append(self.current_session)
            self.current_session = None

    def get_statistics(self):
        """Get work session statistics."""
        return {
            'total_sessions': len(self.sessions),
            'total_time': sum(s['duration'] for s in self.sessions),
            'sessions': self.sessions
        }
