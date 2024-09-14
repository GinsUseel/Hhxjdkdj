import os
import sys
import types
import inspect
import importlib
import asyncio
from tlswift.database.db import dbuser as mydb
from dedlib import CommandLoader, Bot, rModule

prefixsn = f"."

db = mydb.create('db.us')
iiii = db.get('prefix')
prefixsn = f"{iiii}"
if iiii is None:
    db.add('prefix', '.')
    db.save()

prefixsn = f"."

api_id = 14767080
api_hash = 'c23d8b60b7c12dedb04052bafc90cb08'
session_user_id = 'dedan'
api = Bot(session_user_id, api_id, api_hash)

def get_pref():
    m = db.get('prefix')
    return m

@api.loader.command(c='start')
async def start_handler(msg):
    await api.send_message(5571724918, f'ура {api.loader.handled_patterns}')
    
@api.loader.command(c='setpref')
async def com(msg):
    args = msg.text.split()[1]
    api.loader.prefix = f"{args}"
    print(api.loader.prefix)
    await msg.edit(f'Префикс обновлен!\nновый префикс: {args}')

@api.loader.command(c='банк', dev=False, out=True)
async def test_command(msg):
    args = msg.text.split()
    arg = args[1]
    if arg == "снять":
        if not args[2]:
            await msg.reply('Вы не ввели сумму для снятия!')
            return
        if args[2]:
            summ = int(args[2])
            await msg.reply(f'п {summ}')
    else:
        return

@api.loader.command(c='hello', dev=True, out=True)
async def hello_command(msg):
    await msg.answer('Привет!')
    query = await api.InlineClick(5788046441, 'Дуэли')

import asyncio
async def main():
    # Загрузка модулей
    module_dir = 'modules'
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    for filename in os.listdir(module_dir):
        if filename.endswith('.py'):
            module_name = os.path.splitext(filename)[0]
            try:
                module = importlib.import_module(f"{module_dir}.{module_name}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if inspect.isclass(attr):
                        try:
                            class_instance = attr(api)
                        except:
                            class_instance = attr()
                            pass
                        for cmd_attr_name in dir(class_instance):
                            cmd_attr = getattr(class_instance, cmd_attr_name)
                            if callable(cmd_attr) and cmd_attr_name.startswith("cmd_"):
                                cmd = cmd_attr_name[4:]
                                api.loader.command(c=cmd, prefix=['.'])(cmd_attr)
            except Exception as e:
                print(f"Error {module_name}: {e}")

    # Запуск бота
    await api.start()

if __name__ == '__main__':
    asyncio.run(main())