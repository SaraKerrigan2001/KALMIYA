class CustomDashboards:
    def __init__(self):
        self.dashboards = {}
        self.widgets = []

    def create_dashboard(self, dashboard_name):
        """Create a custom dashboard."""
        self.dashboards[dashboard_name] = {
            'name': dashboard_name,
            'widgets': [],
            'layout': 'grid'
        }
        return self.dashboards[dashboard_name]

    def add_widget(self, dashboard_name, widget_type, widget_config):
        """Add a widget to a dashboard."""
        if dashboard_name in self.dashboards:
            widget = {
                'type': widget_type,
                'config': widget_config,
                'position': len(self.dashboards[dashboard_name]['widgets'])
            }
            self.dashboards[dashboard_name]['widgets'].append(widget)

    def remove_widget(self, dashboard_name, widget_index):
        """Remove a widget from dashboard."""
        if dashboard_name in self.dashboards:
            if widget_index < len(self.dashboards[dashboard_name]['widgets']):
                self.dashboards[dashboard_name]['widgets'].pop(widget_index)

    def get_dashboard(self, dashboard_name):
        """Get a dashboard."""
        return self.dashboards.get(dashboard_name)

    def set_default_dashboard(self, dashboard_name):
        """Set default dashboard."""
        return {'default_dashboard': dashboard_name, 'updated': True}
