from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from config import TOKEN
from function import *
from command_buttons import start_keyboard
from inf import *

class Status(StatesGroup):
    start = State()
    convert = State()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())





@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer(f'Добро пожаловать, {message.from_user.first_name}.\nБот готов к тестированию \n/function', reply_markup = start_keyboard)




@dp.message_handler(text = 'Получить реферальную ссылку')
async def start_handler(message: types.Message):
    await message.answer(f'Ваша реферальная ссылка: \n https://1wxuut.top/?open=register&sub1={message.from_user.id}#p4ny', reply_markup = start_keyboard)
    

@dp.message_handler(text='Проверить регистрацию')
async def start_handler(message: types.Message):
    logfun()
    res = check(message.from_user.id)
    await message.answer(f'Результат: \n{res}', reply_markup = start_keyboard)


"""@dp.message_handler(content_types='text')
async def start_handler(message: types.Message):
    print(message.text)
    if message.from_user.id == "-1001874771850":
        print(message.text)
        tech = message.text.split(":::")
        await message.answer(user_id =  tech[0], text = f"{tech[1]}", reply_markup = start_keyboard)
"""


# Модуль для получения инфы из тг канала о регистрациях и депозитах
@dp.channel_post_handler(content_types=['any'])
async def main_handler(message: types.Message):
    tech = message.text.split(":::")
    await message.bot.send_message(chat_id=tech[0], text=f"{tech[1]}", reply_markup=start_keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
