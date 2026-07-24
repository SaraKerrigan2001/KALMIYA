class NavigationHelper:
    def __init__(self):
        self.locations = {}
        self.routes = []

    def set_home(self, address):
        """Set home address."""
        self.locations['home'] = address

    def set_work(self, address):
        """Set work address."""
        self.locations['work'] = address

    def get_directions(self, start, destination, mode='driving'):
        """Get directions between locations."""
        return {
            'start': start,
            'destination': destination,
            'mode': mode,
            'directions': [],
            'distance': None,
            'duration': None
        }

    def get_eta(self, destination):
        """Get estimated time of arrival."""
        return {'destination': destination, 'eta': None}

    def get_traffic_info(self, location):
        """Get real-time traffic information."""
        return {'location': location, 'condition': 'normal'}

    def save_route(self, route_name, waypoints):
        """Save a favorite route."""
        self.routes.append({'name': route_name, 'waypoints': waypoints})
