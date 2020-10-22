from typing import List, Optional, Iterable, Type

from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser
from rest_framework.request import Request
from rest_framework.response import Response

from core.interfaces import Command
from core.entities import UserId
from common.router import Router
from common.serializers import HookSerializer

from notekeeper.commands_deserializers.deserialize_exception import DeserializeException


def response(text: Optional[str]) -> Response:
    return Response() if text is None else Response(dict(text=text))


class SlackHook(GenericAPIView):
    """
    Slack hook handler view
    """

    parser_classes = [FormParser]
    serializer_class = HookSerializer

    router: Router = None

    def __validate_token(self, token: str) -> bool:
        return token == settings.SLACK_TOKEN

    def __get_commands_names(self, commands: Iterable[Type[Command]]) -> List[str]:
        """Returns names of passed command classes, as they are accepted by this view"""
        return list((v for v in self.router.get_command_names(commands).values() if v is not None))

    def __handle_cmd(self, user_id: UserId, bot_name: str, cmd_name: Optional[str], rest: Optional[str]) -> Optional[str]:
        bot = self.router.get_bot(bot_name)
        if bot is None:
            return f"No such bot: {bot_name}, mention one of these bots: {self.router.get_bot_names()}"
        supported_commands = bot.get_supported_commands()
        command_names = self.__get_commands_names(supported_commands)
        supported_commands_names = ', '.join(command_names)
        if cmd_name == 'help':
            if rest is not None:
                if rest in command_names:
                    cmd = self.router.get_command_class(rest)
                    return cmd.__doc__ or "No command description"
                else:
                    return f"Bot {bot_name} doesn't support command {cmd_name}"
            else:
                return f"{bot.__doc__}\nSupported commands: {supported_commands_names}\nSend `{bot_name} help <command>` to get command description"
        else:
            wrapper = self.router.create_wrapper(cmd_name, user_id)
            if wrapper is None:
                return f"Unknown command {cmd_name}, use one of these: {supported_commands_names}"
            if wrapper.command_class in supported_commands:
                try:
                    cmd = wrapper.deserialize(rest)
                except DeserializeException as e:
                    return f"Cannot process command {cmd_name}: {e.description}"
                res = cmd.handle(bot)
                return wrapper.serialize(res)
            else:
                return f"Bot {bot_name} doesn't support command {cmd_name}, only {supported_commands_names}"

    def post(self, request: Request):
        form = self.get_serializer(data=request.data)
        if form.is_valid():
            if not self.__validate_token(form.validated_data.get('token')):
                return response('Invalid auth token')
            user_id = form.validated_data.get('user_id')
            # try to split into bot name, command name and the rest
            splitted = form.validated_data.get('text').split(' ', 2)
            if len(splitted) < 2:
                # TODO: enhance message
                return response(f"You didn't provide command. Send '<botname> help' to get bot description")
            [bot_name, cmd_name] = splitted[0:2]
            res = self.__handle_cmd(user_id, bot_name, cmd_name, None if len(splitted) < 3 else splitted[2])
            if res is not None:
                return response(res)
            else:
                # XXX: is it required?
                return response(f"Command {cmd_name} executed")
        else:
            return response(f"Invalid request:{form.errors}")

