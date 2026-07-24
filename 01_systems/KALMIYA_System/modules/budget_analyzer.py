class BudgetAnalyzer:
    def __init__(self):
        self.budgets = {}
        self.goals = []

    def set_budget(self, category, monthly_limit):
        """Set a budget limit for a category."""
        self.budgets[category] = {'limit': monthly_limit, 'spent': 0}

    def analyze_spending(self, category):
        """Analyze spending patterns for a category."""
        if category in self.budgets:
            budget = self.budgets[category]
            return {
                'category': category,
                'limit': budget['limit'],
                'spent': budget['spent'],
                'remaining': budget['limit'] - budget['spent']
            }

    def get_savings_goal(self, goal_amount, timeline_months):
        """Calculate monthly savings needed for a goal."""
        monthly_savings = goal_amount / timeline_months if timeline_months > 0 else 0
        return {
            'goal': goal_amount,
            'monthly_savings': monthly_savings,
            'timeline': timeline_months
        }
