from aiogram import types

start_botton_1 = types.KeyboardButton('Получить реферальную ссылку')
start_botton_2 = types.KeyboardButton('Проверить регистрацию')

start_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
start_keyboard.add(start_botton_1, start_botton_2)