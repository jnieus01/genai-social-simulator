from chat.command_router import Command

class ShowHelpCommand(Command):
    def __init__(self, router):
        self._router = router

    def execute(self):
        """Display help information for available commands."""
        print("Available commands:")
        for name, command in self._router.list_commands().items():
            print(f"{name}: {command.execute.__doc__}")

class QuitChatCommand(Command):
    
    def execute(self):
        """Exit the chat application."""
        print("Exiting chat. Goodbye!")
        exit(0)