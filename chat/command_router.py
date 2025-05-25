# from chatbot.base_command import Command
from typing import Dict

class Command:
    def execute(self, *args, **kwargs):
        raise NotImplementedError

class CommandRouter:
    def __init__(self):
        self._commands: Dict[str, Command] = {}

    def register(self, name: str, cmd: Command) -> None:
        self._commands[name] = cmd

    def execute(self, name: str, *args):
        cmd = self._commands.get(name)
        if not cmd:
            raise ValueError(f"Unknown command: {name}")
        
        return cmd.execute(*args)

    def list_commands(self) -> Dict[str, Command]:
        return self._commands