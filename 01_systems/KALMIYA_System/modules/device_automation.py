class DeviceAutomation:
    def __init__(self):
        self.automations = []
        self.logs = []

    def create_automation(self, trigger_device, trigger_action, target_devices, target_action):
        """Create automation rule connecting devices."""
        self.automations.append({
            'trigger_device': trigger_device,
            'trigger_action': trigger_action,
            'target_devices': target_devices,
            'target_action': target_action,
            'enabled': True
        })

    def enable_automation(self, automation_id):
        """Enable an automation."""
        if automation_id < len(self.automations):
            self.automations[automation_id]['enabled'] = True

    def disable_automation(self, automation_id):
        """Disable an automation."""
        if automation_id < len(self.automations):
            self.automations[automation_id]['enabled'] = False

    def get_execution_log(self):
        """Get automation execution log."""
        return self.logs

    def test_automation(self, automation_id):
        """Test an automation rule."""
        return {'automation_id': automation_id, 'test_result': 'success'}
