class TripPlanner:
    def __init__(self):
        self.trips = []
        self.itineraries = {}

    def create_trip(self, destination, start_date, end_date, budget=None):
        """Create a new trip."""
        trip = {
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'budget': budget,
            'activities': [],
            'accommodations': []
        }
        self.trips.append(trip)
        return trip

    def add_activity(self, trip_index, activity_name, date, cost=0):
        """Add an activity to trip itinerary."""
        if trip_index < len(self.trips):
            self.trips[trip_index]['activities'].append({
                'name': activity_name,
                'date': date,
                'cost': cost
            })

    def add_accommodation(self, trip_index, hotel_name, check_in, check_out, cost):
        """Add accommodation booking."""
        if trip_index < len(self.trips):
            self.trips[trip_index]['accommodations'].append({
                'name': hotel_name,
                'check_in': check_in,
                'check_out': check_out,
                'cost': cost
            })

    def get_itinerary(self, trip_index):
        """Get complete trip itinerary."""
        if trip_index < len(self.trips):
            return self.trips[trip_index]
