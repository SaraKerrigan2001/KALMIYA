class LightManagement:
    def __init__(self):
        self.lights = {}
        self.schedules = []

    def add_light(self, light_id, light_name, location):
        """Add a smart light."""
        self.lights[light_id] = {
            'name': light_name,
            'location': location,
            'brightness': 100,
            'color': None,
            'on': False
        }

    def control_light(self, light_id, brightness=None, color=None, state=None):
        """Control a light."""
        if light_id in self.lights:
            if brightness is not None:
                self.lights[light_id]['brightness'] = brightness
            if color:
                self.lights[light_id]['color'] = color
            if state is not None:
                self.lights[light_id]['on'] = state
            return self.lights[light_id]

    def set_schedule(self, light_id, time, action):
        """Set light schedule."""
        self.schedules.append({
            'light_id': light_id,
            'time': time,
            'action': action
        })

    def create_scene(self, scene_name, settings):
        """Create a lighting scene."""
        return {'scene': scene_name, 'settings': settings, 'created': True}
