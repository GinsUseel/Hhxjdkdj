# mymodule.py
#author: shshs
#name: dhdh

async def hello_world(msg):
    '''Простая команда для печати приветствия'''
    await msg.answer("Hello, world!")

async def calc(msg):
    '''Команда для вычисления суммы двух чисел'''
    args = msg.get_args.split()
    if len(args) != 2:
        await msg.answer("Используйте: .calc <число1> <число2>")
    else:
        num1 = int(args[0])
        num2 = int(args[1])
        result = num1 + num2
        await msg.answer(f"Результат: {result}")