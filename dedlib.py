import functools
import re
import os
import sys
import types
import importlib
import asyncio
import time
from tlswift.core import *

class rModule:
    _registry = {}

    def __init__(self):
        pass

    @classmethod
    def module(cls, name, description=None, author=None):
        def decorator(module_class):
            if module_class.__name__ != name:
                raise ValueError(f"Class name '{module_class.__name__}' does not match module name '{name}'")
            cls._registry[name] = {'description': description, 'author': author}
            return module_class
        return decorator

class CommandLoader:
    def __init__(self, client, dp):
        self.client = client
        self.handled_patterns = []
        self.command_handlers = {}
        self.inline_callbacks = {}
        self.command_descriptions = {}
        self.event_handlers = {}
        self.wrapper_functions = {}
    
    def command(self, c=None, prefix=['.'], dev=False, out=False, bio=None):
        def decorator(func):
            for p in prefix:
                pattern = "."
                if c is not None:
                    if isinstance(c, list):
                        pattern += "(" + "|".join(c) + ")"
                    else:
                        pattern += c

                if pattern in self.command_handlers:
                    for handler in self.command_handlers[pattern]:
                        self.client.remove_event_handler(handler)
                    del self.command_handlers[pattern]
                    self.handled_patterns.remove(pattern)

                @self.client.on(swift.NewMessage(pattern=pattern))
                async def wrapper(swift):
                    if pattern not in self.handled_patterns:
                        return

                    owner = await self.client.get_me()
                    owner_id = owner.id
                    msg = swift
                    msg.answer = swift.respond
                    msg.from_text = swift.message.text
                    msg.lower = swift.message.text.lower()
                    msg.get_args = swift.raw_text.split(maxsplit=1)[1] if len(swift.raw_text.split()) > 1 else ''
                    str(msg.text.split) == swift.message.text.split

                    if not dev and str(swift.sender_id) != str(owner_id):
                        return

                    try:
                        result = await func(msg)
                    except Exception as e:
                        error_message = f"⚠️ **Ошибка при выполнении команды** `{pattern}`: `{str(e)}`"
                        await msg.edit(error_message)
                        return

                    return result

                self.handled_patterns.append(pattern)
                self.command_handlers[pattern] = [wrapper]
                self.event_handlers[pattern] = wrapper
                self.wrapper_functions[pattern] = wrapper
                if bio:
                    self.command_descriptions[pattern] = bio

            return wrapper

        return decorator

    def remove_command(self, gg):
        pattern = f'.{gg}'
        if pattern in self.command_handlers:
                for handler in self.command_handlers[pattern]:
                        self.client.remove_event_handler(handler)
                del self.command_handlers[pattern]
                self.handled_patterns.remove(pattern)
                if pattern in self.command_descriptions:
                        del self.command_descriptions[pattern]
        else:
            return

    def message(self, only_owner=False):
        def decorator(func):
            @self.client.on(swift.NewMessage())
            async def handle_message(swift):
                if only_owner:
                    owner = await self.client.get_me()
                    owner_id = owner.id
                    if str(swift.sender_id) != str(owner_id):
                        return

                msg = swift
                message = swift
                msg.answer = swift.respond
                msg.text = swift.message.text
                msg.lower = swift.message.text.lower()
                str(msg.text.split) == swift.message.text.split

                await func(msg)

            return func

        return decorator

class Bot(TelegramClient):
    msg = events
    def __init__(self, session_name, api_id, api_hash):
        super().__init__(session_name, api_id, api_hash)
        self.loader = CommandLoader(self, None)

    async def start(self):
        try:
           print('Connected')
           await super().start()
           await self.run_until_disconnected()
        except:
            print('Stopped')

    async def InlineQueryResult(self, bot, peer, query, offset, geo_point):
        inline_query_result = await self(GetInlineBotResultsRequest(
            bot=bot,
            peer=peer,
            query=query,
            offset=offset,
            geo_point=geo_point
        ))
        return inline_query_result

    async def InlineQuery(self, bot, text):
        inline_query = await self.inline_query(bot, text)

        return inline_query

    async def InlineClick(self, chat_id, textv):
        try:
            messages = await self.get_messages(chat_id, limit=1)

            inf = await messages[0].click(text=textv)
            return inf
        except ChannelPrivateError:
            print("This chat doesn't allow private messages.")
            return False
        except IndexError:
            print("Invalid button index.")
            return False