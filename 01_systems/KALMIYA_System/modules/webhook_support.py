class WebhookSupport:
    def __init__(self):
        self.webhooks = {}
        self.event_log = []

    def register_webhook(self, webhook_name, trigger_event, endpoint_url):
        """Register a webhook."""
        self.webhooks[webhook_name] = {
            'event': trigger_event,
            'endpoint': endpoint_url,
            'active': True,
            'created_time': None
        }
        return {'webhook': webhook_name, 'registered': True}

    def trigger_webhook(self, event_type, data=None):
        """Trigger webhooks for an event."""
        triggered = []
        for name, webhook in self.webhooks.items():
            if webhook['event'] == event_type and webhook['active']:
                triggered.append(name)

        self.event_log.append({
            'event': event_type,
            'triggered_webhooks': triggered,
            'timestamp': None
        })
        return {'event': event_type, 'triggered': triggered}

    def disable_webhook(self, webhook_name):
        """Disable a webhook."""
        if webhook_name in self.webhooks:
            self.webhooks[webhook_name]['active'] = False
            return {'webhook': webhook_name, 'disabled': True}

    def get_event_log(self):
        """Get webhook event log."""
        return self.event_log

    def delete_webhook(self, webhook_name):
        """Delete a webhook."""
        if webhook_name in self.webhooks:
            del self.webhooks[webhook_name]
            return {'webhook': webhook_name, 'deleted': True}
