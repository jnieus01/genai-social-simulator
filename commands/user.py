from chat.command_router import Command

class IdentifyUserCommand(Command):
    def __init__(self, user_service):
        self.svc = user_service

    def execute(self, *args):
        """Enter your info."""
        name, age, location = args[0], args[1], args[2]
        return self.svc.save_user(name, age, location)

class ShowUserInfoCommand(Command):
    def __init__(self, user_service):
        self._svc = user_service

    def execute(self, name=None):
        """Show user info."""
        if not name:
            return "Please provide a username."
        return self._svc.get_user(name)

class ListUsersCommand(Command):
    def __init__(self, user_service):
        self._svc = user_service

    def execute(self):
        """List all users on the chat app."""
        return self._svc.get_all_users()