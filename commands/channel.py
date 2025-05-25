from chat.command_router import Command

class JoinChannelCommand(Command):
    def __init__(self, channel_service):
        self._svc = channel_service

    def execute(self, channels: list[str]) -> list[str]:
        """Subscribe current user to a Redis channel."""
        return self._svc.join_channels(channels)

class ListenCommand(Command):
    def __init__(self, channel_service):
        self._svc = channel_service

    def execute(self, channel: str | None) -> None:
        """Listen for messages on subscribed channels."""
        return self._svc.listen(channel=channel)

class LeaveChannelCommand(Command):
    def __init__(self, channel_service):
        self._svc = channel_service

    def execute(self, channel: str = None) -> str:
        """Unsubscribe from a Redis channel."""
        return self._svc.leave_channels(channel=channel)
    
class ListUserChannelsCommand(Command):
    def __init__(self, channel_service):
        self._svc = channel_service

    def execute(self) -> list[str]:
        """List all channels the user is subscribed to."""
        return self._svc.get_user_channels()

class ListAllChannelsCommand(Command):
    def __init__(self, channel_service):
        self._svc = channel_service

    def execute(self, channels: list[str] = None) -> list[str]:
        return self._svc.list_all_channels(channels)