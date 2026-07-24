class MultiLanguageSupport:
    def __init__(self):
        self.languages = []
        self.translations = {}

    def add_language(self, language_code, language_name):
        """Add a supported language."""
        self.languages.append({
            'code': language_code,
            'name': language_name
        })

    def set_interface_language(self, language_code):
        """Set the interface language."""
        return {'interface_language': language_code, 'applied': True}

    def get_available_languages(self):
        """Get all available languages."""
        return self.languages

    def translate_text(self, text, source_lang, target_lang):
        """Translate text between languages."""
        return {
            'original': text,
            'source': source_lang,
            'target': target_lang,
            'translated': None
        }
