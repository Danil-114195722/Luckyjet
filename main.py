import asyncio

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from data.config import TOKEN
from utils.keyboard import inline_choose_rate, inline_join_group, main_keyboard, inline_buy_rate
from utils.db_connection import create_table_user, \
    select_user, add_user, \
    make_reg, make_rate


bot = Bot(token=TOKEN)
storage = MemoryStorage()
disp = Dispatcher(bot=bot, storage=storage)


# класс состояния
class RegState(StatesGroup):
    user_id = State()
    chosen_rate = State()
    start_reg = State()


'''
$$$$$$$$$$$$$$$
БАЗОВЫЕ ФУНКЦИИ
$$$$$$$$$$$$$$$
'''


async def check_reg_func(user_id: int):
    reg_status = select_user(tg_id=user_id)[2]
    print(reg_status)
    if reg_status:
        return True

    # здесь Никита проверяет переход по ссылке на регистрацию
    nikita_check_reg_link = False
    # если юзер переходил по ссылке, то добавляем инфу о регистрации в БД
    if nikita_check_reg_link:
        make_reg(tg_id=user_id)
        return True

    return False


async def check_deposit_func(user_id: int):
    rate = select_user(tg_id=user_id)[3]

    if rate is not None:
        return True

    # здесь Никита проверяет переход по ссылке на оплату депозита
    nikita_check_reg_link = False
    # если юзер переходил по ссылке, то добавляем инфу об оплате в БД
    if nikita_check_reg_link:
        nikita_rate_status = 0
        make_rate(tg_id=user_id, rate=nikita_rate_status)
        return True

    return False


# функция, выполняемая при включении бота
async def on_startup(disp):
    # создаём таблицу "user"
    create_table_user()


# выбор тарифа
@disp.message_handler(commands='start', state='*')
async def start_command(message: types.Message, state: FSMContext):
    await state.finish()

    user_id = message.from_user.id

    await RegState.user_id.set()
    await state.update_data(user_id=user_id)

    # добавление юзера в БД
    if not select_user(tg_id=user_id):
        add_user(tg_id=user_id, reg=False)

    photo = types.InputFile("./img/select_rate.jpeg")
    await bot.send_photo(chat_id=user_id, photo=photo, caption='Выбери тариф:', reply_markup=inline_choose_rate)

    await RegState.chosen_rate.set()
    # await start(callback=message, state=state)


'''
$$$$$$$$$$$$$$$$$$$
ФУНКЦИИ РЕГИСТРАЦИИ
$$$$$$$$$$$$$$$$$$$
'''


# начать
@disp.callback_query_handler(state=RegState.chosen_rate, text=['always', 'month', 'free'])
# @disp.callback_query_handler(state=RegState.chosen_rate)
async def start(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    photo = types.InputFile("./img/start_reg.jpeg")
    await bot.send_photo(
        chat_id=state_data["user_id"],
        photo=photo,
        caption='''Привет!
Как я понимаю ты хочешь получить доступ в мой ЗАКРЫТЫЙ ВИП КАНАЛ с сигналами для игры в LuckyJet?
Это БЕСПЛАТНО
За 1 неделю ты успеешь заработать на месячный доступ к моему ВИП КАНАЛУ
Нужно сделать ряд простых условий и начать зарабатывать!
Если ты готов - нажми кнопку НАЧАТЬ ниже''',
        reply_markup=inline_join_group
    )

    await RegState.start_reg.set()


# регистрация
@disp.callback_query_handler(state=RegState.start_reg, text='start')
async def start_reg(callback: CallbackQuery, state: FSMContext, fail_reg: bool = False):
    state_data = await state.get_data()

    if not fail_reg:
        photo = types.InputFile("./img/reg_new_acc.jpeg")
        await bot.send_photo(
            chat_id=state_data["user_id"],
            photo=photo,
            caption='''📲Для начала необходимо провести регистрацию на 1win (провайдер игры LuckyJet). Чтобы бот успешно проверил регистрацию, нужно соблюсти важные условия:
\n1️⃣Аккаунт обязательно должен быть НОВЫМ! Если у вас уже есть аккаунт и при нажатии на кнопку «РЕГИСТРАЦИЯ» вы попадаете на старый, необходимо выйти с него и заново нажать на кнопку «РЕГИСТРАЦИЯ», после чего по новой зарегистрироваться!
\n2️⃣Чтобы бот смог проверить вашу регистрацию, обязательно нужно ввести промокод CRYPA при регистрации!''',
            reply_markup=main_keyboard
        )

    else:
        photo = types.InputFile("./img/reg_reject.jpeg")
        await bot.send_photo(
            chat_id=state_data["user_id"],
            photo=photo,
            caption='''❌РЕГИСТРАЦИЯ НЕ ПРОЙДЕНА\n\n📲Для начала необходимо провести регистрацию на 1win (провайдер игры LuckyJet). Чтобы бот успешно проверил регистрацию, нужно соблюсти важные условия:
\n1️⃣Аккаунт обязательно должен быть НОВЫМ! Если у вас уже есть аккаунт и при нажатии на кнопку «РЕГИСТРАЦИЯ» вы попадаете на старый, необходимо выйти с него и заново нажать на кнопку «РЕГИСТРАЦИЯ», после чего по новой зарегистрироваться!
\n2️⃣Чтобы бот смог проверить вашу регистрацию, обязательно нужно ввести промокод CRYPA при регистрации!
⚠️Как ввести промокод можно узнать здесь: https://t.me/c/1800027834/307
\nПосле РЕГИСТРАЦИИ бот автоматически переведёт вас к следующему шагу✅''',
            reply_markup=main_keyboard
        )


# проверка регистрации
@disp.callback_query_handler(state=RegState.start_reg, text='check_reg')
async def check_reg(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    reg = await check_reg_func(user_id=state_data["user_id"])

    if reg:
        await deposit(callback=callback, state=state)
    else:
        await start_reg(callback=callback, state=state, fail_reg=True)


# оплата депозита
async def deposit(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    photo = types.InputFile("./img/reg_done.jpeg")
    await bot.send_photo(
        chat_id=state_data["user_id"],
        photo=photo,
        caption='''✅РЕГИСТРАЦИЯ УСПЕШНА!\n\n‼️Для того, чтобы получить доступ в закрытую группу с сигналами, необходимо на любую сумму пополнить баланс аккаунта, который вы только что зарегистрировали.
На эти деньги вы будете делать ставки по сигналам.
Нажми на кнопку ПОПОЛНИТЬ ДЕПОЗИТ и тебе откроет 1WIN.
\n✅После успешного пополнения бот АВТОМАТИЧЕСКИ выдаст вам ссылку на вступление в группу''',
        reply_markup=inline_buy_rate
    )


# проверка оплаты депозита
@disp.callback_query_handler(state=RegState.start_reg, text='check_paid')
async def check_paid(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    rate_paid = await check_deposit_func(user_id=state_data["user_id"])

    if rate_paid:
        await bot.send_message(
            chat_id=state_data["user_id"],
            text='''Добро пожаловать в ВИП-чат! Вот ссылка на вход - https://t.me/+IwQ9bT41nzBiN2Yy
Если будут какие-то вопросы, то пиши мне @strategvlad''',
            reply_markup=main_keyboard
        )
    else:
        await deposit(callback=callback, state=state)


if __name__ == '__main__':
    executor.start_polling(disp, skip_updates=True, on_startup=on_startup)
