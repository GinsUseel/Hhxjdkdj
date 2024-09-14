import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Создание экземпляра бота
bot = Bot(token='7001866832:AAGbeBUAoMKyx74pZMg2FCzawwKvihv8XFQ')
dp = Dispatcher(bot, storage=MemoryStorage())

# Словарь для хранения инлайн-команд и клавиатур
inlines = {}

# Функция для создания инлайн-клавиатуры
async def InlineCall(**buttons):
    inline_keyboard = types.InlineKeyboardMarkup()
    for button_name, button_data in buttons.items():
        button = types.InlineKeyboardButton(
            text=button_data['text'],
            callback_data=button_data['callback']
        )
        inline_keyboard.add(button)
    return inline_keyboard

# Функция для регистрации инлайн-команды
def RegisterInlineCommand(command, keyboard):
    inlines[command] = {'keyboard': keyboard}

# Обработчик для инлайн-запросов
@dp.inline_handler(lambda query: query.query in inlines)
async def inline_handler(query: types.InlineQuery):
    inline_data = inlines.get(query.query)
    if inline_data:
        result = [types.InlineQueryResultArticle(
            id='1',
            title='Отправить инлайн',
            input_message_content=types.InputTextMessageContent(
                message_text='Результат инлайн-команды'
            ),
            reply_markup=inline_data['keyboard']
        )]
        await query.answer(results=result, cache_time=60)

# Обработчики для callback-запросов
@dp.callback_query_handler(lambda call: any(call.data.startswith(key) for key in inlines))
async def callback_handler(call: types.CallbackQuery):
    for command, data in inlines.items():
        if call.data.startswith(command):
            callback_data = call.data.replace(command + ':', '')
            await call.answer(f'Вы нажали кнопку "{callback_data}"')
            break

# Запуск бота
async def start_bot():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(start_bot())