class LanguageLearning:
    def __init__(self):
        self.languages = {}
        self.lessons = []

    def add_language(self, language_code, language_name):
        """Add a language to learn."""
        self.languages[language_code] = {'name': language_name, 'progress': 0}

    def start_lesson(self, language_code, lesson_type):
        """Start a language lesson."""
        self.lessons.append({
            'language': language_code,
            'type': lesson_type,
            'completed': False
        })

    def get_progress(self, language_code):
        """Get learning progress for a language."""
        return self.languages.get(language_code, {})

    def get_daily_goal(self):
        """Get daily learning goals."""
        return {'minutes': 15, 'lessons': 1}
