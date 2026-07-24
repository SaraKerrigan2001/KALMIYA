class SmartHomeControl:
    def __init__(self):
        self.devices = {}
        self.automations = []

    def add_device(self, device_id, device_name, device_type):
        """Add a smart home device."""
        self.devices[device_id] = {
            'name': device_name,
            'type': device_type,
            'status': 'offline'
        }

    def control_device(self, device_id, action, parameters=None):
        """Control a smart home device."""
        if device_id in self.devices:
            return {
                'device': device_id,
                'action': action,
                'status': 'executed'
            }

    def create_automation(self, trigger, action, name=None):
        """Create an automation rule."""
        self.automations.append({
            'name': name,
            'trigger': trigger,
            'action': action,
            'enabled': True
        })

    def get_device_status(self, device_id=None):
        """Get status of devices."""
        if device_id:
            return self.devices.get(device_id)
        return self.devices
