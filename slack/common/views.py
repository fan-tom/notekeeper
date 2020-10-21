from typing import List, Optional, Iterable, Type

from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser
from rest_framework.request import Request
from rest_framework.response import Response

from core.commands import Push, Top
from core.interfaces import Command
from core.note import UserId
from common import Router
from common.serializers import HookSerializer
from django.conf import settings


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
        print(f'validating token: {token}')
        return token == settings.SLACK_TOKEN

    def __get_commands_names(self, commands: Iterable[Type[Command]]) -> List[str]:
        """Returns names of passed command classes, as they are accepted by this view"""
        return list(map(lambda v: v[1], filter(lambda v: v[1] is not None, self.router.get_command_names(commands).items())))

    def __handle_cmd(self, user_id: UserId, bot_name: str, cmd_name: Optional[str], rest: Optional[str]) -> Optional[str]:
        bot = self.router.get_bot(bot_name)
        if bot is None:
            return f"No such bot: {bot_name}, mention one of these bots: {self.router.get_bot_names()}"
        supported_commands = bot.get_supported_commands()
        command_names = self.__get_commands_names(supported_commands)
        if cmd_name == 'help':
            if rest is not None:
                if rest in command_names:
                    cmd = self.router.get_command_class(rest)
                    return cmd.__doc__ or "No command description"
                else:
                    return f"Bot {bot_name} doesn't support command {cmd_name}"
            else:
                return f"{bot.__doc__}\nSupported commands: {', '.join(command_names)}\nSend `{bot_name} help <command>` to get command description"
        else:
            if len(supported_commands) > 0:
                if cmd_name == 'push':
                    if rest is None:
                        return f"Command '{cmd_name}' requires note text"
                    note = Push(user_id, rest).handle(bot)
                    return f"Note was saved with id {note.id}"
                elif cmd_name == 'top':
                    if rest is None:
                        n = None
                    else:
                        try:
                            n = int(rest)
                        except ValueError:
                            return f"Command '{cmd_name}' accepts numeric argument, got {rest}"
                    notes = Top(user_id, n).handle(bot)
                    content = '\n\n'.join(map(lambda note: f"Id: {note.id}\nCreated at: {note.created_at}\nText: {note.text}", notes))
                    return f"Last {'note' if n is None else f'{len(notes)} notes'}:\n\n{content}"
                else:
                    return f"Bot {bot_name} doesn't support command {cmd_name}, only {command_names}"
            elif cmd_name is not None:
                return f"Bot {bot_name} doesn't support any command"
            else:
                return f"Bot {bot_name} doesn't support any command and no command was provided'"

    def post(self, request: Request):
        form: HookSerializer = self.get_serializer(data=request.data)
        if form.is_valid():
            if not self.__validate_token(form.validated_data.get('token')):
                return response('Invalid auth token')
            user_id = form.validated_data.get('user_id')
            # try to split into bot name, command name and the rest
            splitted: List[str] = form.validated_data.get('text').split(' ', 2)
            if len(splitted) < 2:
                # TODO: enhance message
                return response(f"You didn't provide command. Send '<botname> help' to get bot description")
            [bot_name, cmd_name] = splitted[0:2]
            print(f"Handling: {bot_name}:{cmd_name}")
            res = self.__handle_cmd(user_id, bot_name, cmd_name, None if len(splitted) < 3 else splitted[2])
            print(f"Command processing result: {res}")
            if res is not None:
                return response(res)
            else:
                # XXX: is it required?
                return response(f"Command {cmd_name} executed")
        else:
            return response(f"Invalid request:{form.errors}")

