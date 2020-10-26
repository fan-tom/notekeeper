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

from notekeeper.commands_deserializers import DeserializeException


def response(text: Optional[str] = None) -> Response:
    # REVIEW M1ha: Зачем плодить сущности без необходимости?
    #  Почему вместо использования этой функции нельзя просто вернуть Response({'text': 'my message'})
    #  или Response() в зависимости от ситуации?
    return Response() if text is None else Response(dict(text=text))


class SlackHook(GenericAPIView):
    """
    Slack hook handler view
    """

    parser_classes = [FormParser]
    serializer_class = HookSerializer

    # REVIEW M1ha: На мой взгляд с роутером какая-то очень непрозрачная схема.
    #  Плюс роутер должен делать что-то одно: выбирать БД, выбирать бота. А тут все валено в кучу: и команды, и боты,
    #  и какие-то неведомые обертки и какие-то сервисные методы рожденные сложностью всех этих оберток.
    router: Router = None

    def __validate_token(self, token: str) -> bool:
        # REVIEW M1ha: С одной стороны, плюс, за то, что сделана проверка токена. Б - Безопасность.
        #  С другой стороны - минус, потому что проверка не расширяема. Если я захочу в одном проекте сделать 2 ботов,
        #  то либо мне надо будет указывать общий токен, либо переписывать это.
        return token == settings.SLACK_TOKEN

    def __get_commands_names(self, commands: Iterable[Type[Command]]) -> List[str]:
        """Returns names of passed command classes, as they are accepted by this view"""
        # REVIEW M1ha: Лишние скобки это важно. По файту, ты здесь создал генератор, а из него список.
        #   Можно было гораздо проще:
        #   return [v for v in self.router.get_command_names(commands).values() if v is not None]
        return list((v for v in self.router.get_command_names(commands).values() if v is not None))

    def __handle_cmd(self, user_id: UserId, bot_name: str, cmd_name: Optional[str], rest: Optional[str]) -> Optional[str]:
        bot = self.router.get_bot(bot_name)
        if bot is None:
            return f"No such bot: {bot_name}, mention one of these bots: {self.router.get_bot_names()}"
        supported_commands = bot.get_supported_commands()

        # REVIEW M1ha:
        #   1. Зачем это делать здесь, если эти переменные нужны только внутри help-а?
        #     Зачем лишние действия на каждую команду?
        #   2. Зачем выделять это в отдельный метод, если он элементарен в реализации и нигде больше не используется?
        command_names = self.__get_commands_names(supported_commands)
        supported_commands_names = ', '.join(command_names)

        # REVIEW M1ha: А почему не сделать help обычной командой с общим интерфейсом?
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
            # NOTE M1ha: Насколько я понимаю, create_wrapper возвращает wrapper, содержащий команду по её имени
            # REVIEW M1ha:
            #   1. Что за wrapper? Что он делает? Из имен ничего не ясно, код не самодокументируем
            #   2. У разных ботов могут быть команды с одинаковым именем, которые делают разные вещи - плохо расширяемо
            wrapper = self.router.create_wrapper(cmd_name, user_id)
            if wrapper is None:
                return f"Unknown command {cmd_name}, use one of these: {supported_commands_names}"
            if wrapper.command_class in supported_commands:
                try:
                    # REVIEW M1ha: deserialize плохое имя, потому что обобщенное и не говорит, а что вообще тут делается.
                    #  Было бы логичнее и нагляднее, parse_arguments, например.
                    cmd = wrapper.deserialize(rest)
                except DeserializeException as e:
                    return f"Cannot process command {cmd_name}: {e.description}"
                res = cmd.handle(bot)

                # REVIEW M1ha. Опять же, что это делает? Зачем?
                return wrapper.serialize(res)
            else:
                return f"Bot {bot_name} doesn't support command {cmd_name}, only {supported_commands_names}"

    def post(self, request: Request):
        # REVIEW M1ha: для одной view, валидацию так можно сделать.
        #  Но в большом проекте view будет много и это будет плодить кучу ненужного кода.
        #  Красивая схема - это:
        #    1. Добавить обработку ValidationError в APIView
        #    2. Добавить к APIView атрибут validation_serializers = [] (ни или примерно так, там могут быть нюансы)
        #    3. Как вариант, можно написать декоратор @validate_serizliers(...), который будет поднимать исключение.
        #  Ко всему прочему, это позволит стандартизировать ошибки
        form = self.get_serializer(data=request.data)
        if form.is_valid():
            if not self.__validate_token(form.validated_data.get('token')):
                # REVIEW M1ha: Почему response пустой? Тут должна быть ошибка API со status = 401/403.
                #  Иначе заколебешься понимать, почему у тебя это не работает.
                return response()

            user_id = form.validated_data.get('user_id')
            # try to split into bot name, command name and the rest
            #  REVIEW M1ha: Практика показывает, что разделители могут быть не только в виде пробелов.
            splitted = form.validated_data.get('text').split(' ', 2)
            if len(splitted) < 2:
                # TODO: enhance message
                # REVIEW M1ha: Тут лучше подставлять имя бота, следуя концепции, что пользователь - дебил.
                return response(f"You didn't provide command. Send '<botname> help' to get bot description")

            # REVIEW M1ha: [] не нужны. Это создает массив, используя лишнюю память.
            #  Стилистика python вообще не любит лишних скобок.
            #  bot_name, cmd_name = splitted[:2]
            [bot_name, cmd_name] = splitted[0:2]
            res = self.__handle_cmd(user_id, bot_name, cmd_name, None if len(splitted) < 3 else splitted[2])
            if res is not None:
                return response(res)
            else:
                # XXX: is it required?
                # REVIEW M1ha: Мне странно, что команда может не иметь обратной связи.
                #  Но ОК, плюс за обработку потенциального бага.
                return response(f"Command {cmd_name} executed")
        else:
            return response(f"Invalid request:{form.errors}")

