from chat.command_router import Command

class SendMessageCommand(Command):
    def __init__(self, message_service):
        self._svc = message_service

    def execute(self, channel=None, message=None):
        """Send a message to a channel."""
        return self._svc.send_to_channel(channel, message)

class SendDirectMessageCommand(Command):
    def __init__(self, message_service):
        self._svc = message_service

    def execute(self, recipient_username=None, message=None):
        """Send a direct message to a user."""
        return self._svc.send_direct_message(recipient_username, message)