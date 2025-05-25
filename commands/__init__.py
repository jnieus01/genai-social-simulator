from commands.user import IdentifyUserCommand, ShowUserInfoCommand, ListUsersCommand
from commands.channel import JoinChannelCommand, ListenCommand, LeaveChannelCommand, ListAllChannelsCommand, ListUserChannelsCommand
from commands.message import SendMessageCommand, SendDirectMessageCommand
from commands.app import ShowHelpCommand, QuitChatCommand


__all__ = [
    "IdentifyUserCommand", "ShowUserInfoCommand", "ListUsersCommand",
    "JoinChannelCommand", "ListenCommand", "LeaveChannelCommand", "ListAllChannelsCommand", "ListUserChannelsCommand",
    "SendMessageCommand", "SendDirectMessageCommand",
    "ShowHelpCommand", "QuitChatCommand"
]

def register_all(router, chatbot):
    router.register("identify", IdentifyUserCommand(chatbot._user_service))
    router.register("list all channels", ListAllChannelsCommand(chatbot._channel_service))
    router.register("list my channels", ListUserChannelsCommand(chatbot._channel_service))
    router.register("listen", ListenCommand(chatbot._channel_service))
    router.register("join", JoinChannelCommand(chatbot._channel_service))
    router.register("leave", LeaveChannelCommand(chatbot._channel_service))
    router.register("send", SendMessageCommand(chatbot._message_service))
    router.register("dm", SendDirectMessageCommand(chatbot._message_service))
    router.register("whoami", ShowUserInfoCommand(chatbot._user_service))
    router.register("!help", ShowHelpCommand(router))
    router.register("quit", QuitChatCommand())
