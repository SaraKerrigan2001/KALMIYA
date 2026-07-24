class ReminderSystem:
    def __init__(self):
        self.reminders = []

    def set_reminder(self, reminder_text, trigger_time, priority='normal'):
        """Create a new reminder."""
        self.reminders.append({
            'text': reminder_text,
            'time': trigger_time,
            'priority': priority,
            'triggered': False
        })

    def get_active_reminders(self):
        """Get all active reminders."""
        return [r for r in self.reminders if not r['triggered']]

    def trigger_reminder(self, reminder_index):
        """Trigger a reminder."""
        if reminder_index < len(self.reminders):
            self.reminders[reminder_index]['triggered'] = True

    def snooze_reminder(self, reminder_index, minutes=5):
        """Snooze a reminder for specified minutes."""
        return {'snoozed': True, 'minutes': minutes}
