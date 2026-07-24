class TravelBudget:
    def __init__(self):
        self.budgets = {}
        self.expenses = []

    def set_budget(self, trip_name, total_budget):
        """Set budget for a trip."""
        self.budgets[trip_name] = {
            'total': total_budget,
            'spent': 0,
            'breakdown': {}
        }

    def add_expense(self, trip_name, category, amount, description=''):
        """Add expense to trip budget."""
        self.expenses.append({
            'trip': trip_name,
            'category': category,
            'amount': amount,
            'description': description
        })

    def get_budget_status(self, trip_name):
        """Get budget status for a trip."""
        if trip_name in self.budgets:
            budget = self.budgets[trip_name]
            return {
                'trip': trip_name,
                'total': budget['total'],
                'spent': budget['spent'],
                'remaining': budget['total'] - budget['spent']
            }

    def get_expense_breakdown(self, trip_name):
        """Get expense breakdown by category."""
        return {
            'trip': trip_name,
            'breakdown': {}
        }
