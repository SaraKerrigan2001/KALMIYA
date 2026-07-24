class TODOManager:
    def __init__(self):
        self.todos = {}

    def add_todo(self, task_id, task_name, priority='medium', due_date=None):
        """Add a new task to the todo list."""
        self.todos[task_id] = {
            'name': task_name,
            'priority': priority,
            'due_date': due_date,
            'completed': False
        }

    def get_priority_order(self):
        """Return todos sorted by priority."""
        priority_map = {'high': 0, 'medium': 1, 'low': 2}
        return sorted(self.todos.items(), key=lambda x: priority_map.get(x[1]['priority'], 3))

    def complete_todo(self, task_id):
        """Mark a task as completed."""
        if task_id in self.todos:
            self.todos[task_id]['completed'] = True

    def get_daily_summary(self):
        """Get summary of today's tasks."""
        return [t for t in self.todos.values() if not t['completed']]
