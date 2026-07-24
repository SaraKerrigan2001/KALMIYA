class TemperatureControl:
    def __init__(self):
        self.thermostats = {}
        self.schedules = []

    def add_thermostat(self, thermostat_id, location):
        """Add a smart thermostat."""
        self.thermostats[thermostat_id] = {
            'location': location,
            'current_temp': None,
            'target_temp': 70,
            'mode': 'auto',
            'status': 'idle'
        }

    def set_temperature(self, thermostat_id, target_temp):
        """Set target temperature."""
        if thermostat_id in self.thermostats:
            self.thermostats[thermostat_id]['target_temp'] = target_temp

    def set_mode(self, thermostat_id, mode):
        """Set thermostat mode (heat, cool, auto, off)."""
        if thermostat_id in self.thermostats:
            self.thermostats[thermostat_id]['mode'] = mode

    def create_schedule(self, thermostat_id, time, temperature):
        """Create temperature schedule."""
        self.schedules.append({
            'thermostat_id': thermostat_id,
            'time': time,
            'temperature': temperature
        })

    def get_temperature(self, thermostat_id):
        """Get current temperature reading."""
        if thermostat_id in self.thermostats:
            return self.thermostats[thermostat_id]['current_temp']
