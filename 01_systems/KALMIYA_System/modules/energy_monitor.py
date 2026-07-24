class EnergyMonitor:
    def __init__(self):
        self.devices = {}
        self.usage_log = []
        self.goals = {}

    def add_device(self, device_id, device_name):
        """Add device to energy monitoring."""
        self.devices[device_id] = {
            'name': device_name,
            'current_usage': 0,
            'status': 'off'
        }

    def log_usage(self, device_id, wattage, duration):
        """Log energy usage."""
        self.usage_log.append({
            'device_id': device_id,
            'wattage': wattage,
            'duration': duration,
            'timestamp': None
        })

    def get_usage_report(self, period='monthly'):
        """Get energy usage report."""
        return {'period': period, 'total_usage': 0, 'by_device': {}}

    def set_consumption_goal(self, goal_kwh):
        """Set energy consumption goal."""
        self.goals['monthly'] = goal_kwh

    def get_consumption_status(self):
        """Get current consumption vs goal."""
        return {'current': 0, 'goal': self.goals.get('monthly'), 'remaining': 0}
