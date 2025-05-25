from dataclasses import dataclass
from typing import Callable, Sequence, Any

from chat.command_router import CommandRouter
from commands import *
from services import *


## helpers
def prompt_many(*questions: str) -> list[str]:
    """Ask each question, return the answers in order."""
    return [input(q) for q in questions]

@dataclass
class CommandSpec:
    prompts: Sequence[str]                           # questions to ask
    args_builder: Callable[[list[str]], tuple]       # answers -> *args
    presenter: Callable[[Any], None]                 # result -> print()


## router and commands
def build_router(services) -> tuple[CommandRouter, dict[str, CommandSpec]]:
    router = CommandRouter()

    channel_cmds = {
        "join": (
            JoinChannelCommand(services.channel),
            CommandSpec(
                prompts=("Channels to join (comma-separated): ",),
                args_builder=lambda a: ( [c.strip() for c in a[0].split(",")], ),
                presenter=lambda result: print("Joined:", ", ".join(result))
            )
        ),
        "listen": (
            ListenCommand(services.channel),
            CommandSpec(
                prompts=("Channel to listen to: ",),
                args_builder=lambda a: (a[0].strip(),),
                presenter=lambda _: None          # channel_service prints live msgs
            )
        ),
        "leave": (
            LeaveChannelCommand(services.channel),
            CommandSpec(
                prompts=("Channel to leave: ",),
                args_builder=lambda a: (a[0].strip(),),
                presenter=lambda result: print("Left channel:", result)
            )
            
        ),
        "list_channels": (
            ListUserChannelsCommand(services.channel),
            CommandSpec(
                prompts=(),
                args_builder=lambda _: tuple(),
                presenter=lambda channels: print("\n".join(channels) or "No channels.")
            )
        ),
        "list_all_channels": (
            ListAllChannelsCommand(services.channel),
            CommandSpec(
                prompts=("Channels to list (optional, comma-separated): ",),
                args_builder=lambda a: ( [c.strip() for c in a[0].split(",")] if a[0] else None, ),
                presenter=lambda channels: print("\n".join(channels) or "No channels.")
            )
        ),
    }

    message_cmds = {
        "say": (
            SendMessageCommand(services.message),
            CommandSpec(
                prompts=("Channel: ", "Message: "),
                args_builder=lambda a: (a[0], a[1]),
                presenter=lambda _: print("Message sent.")
            )
        ),
        "dm": (
            SendDirectMessageCommand(services.message),
            CommandSpec(
                prompts=("User: ", "Message: "),
                args_builder=lambda a: (a[0], a[1]),
                presenter=lambda _: print("DM sent.")
            )
        ),
    }

    user_cmds = {
        "self_identify": (
            IdentifyUserCommand(services.user),
            CommandSpec(
                prompts=("Name: ", "Age: ", "Location: "),
                args_builder=lambda a: (a[0], a[1], a[2]),
                presenter=lambda _: print("User info saved."),
            ),
        ),
        "whoami": (
            ShowUserInfoCommand(services.user),
            CommandSpec(
                prompts=("Name: ",),
                args_builder=lambda a: (a[0],),
                presenter=lambda user: print(user or "No such user.")
            )
        ),
        "users": (
            ListUsersCommand(services.user),
            CommandSpec(
                prompts=(),
                args_builder=lambda _: tuple(),
                presenter=lambda users: print("\n".join(map(str, users)) or "No users.")
            )
        ),
    }

    meta_cmds = {
        "help": (
            ShowHelpCommand(router),
            CommandSpec(
                prompts=(),
                args_builder=lambda _: tuple(),
                presenter=lambda _: None
            )
        ),
        "quit": (
            QuitChatCommand(),
            CommandSpec(
                prompts=(),
                args_builder=lambda _: tuple(),
                presenter=lambda _: None
            )
        ),
    }

    # register every command with the router & build a lookup of specs
    specs: dict[str, CommandSpec] = {}
    for name, (cmd, spec) in (
        channel_cmds | message_cmds | user_cmds | meta_cmds
    ).items():
        router.register(name, cmd)
        specs[name] = spec

    return router, specs

## main loop 
def main(services) -> None:
    router, specs = build_router(services)

    print("Welcome to Chat!  Type 'help' for commands, and control-C to exit.\n")
    while True:
        try:
            choice = input("\n> ").strip()
            if choice not in specs:
                print("Unknown command.")
                continue

            spec = specs[choice]
            answers = prompt_many(*spec.prompts)
            args = spec.args_builder(answers)
            result = router.execute(choice, *args)
            spec.presenter(result)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    import redis, types, config # type: ignore
    client = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    pubsub = client.pubsub()

    services = types.SimpleNamespace(
        user    = UserService(client),
        channel = ChannelService(client, pubsub, username="me"),
        message = MessageService(client, pubsub, username="me"),
    )

    main(services)