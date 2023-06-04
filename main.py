import asyncio

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from data.config import TOKEN
from utils.keyboard import main_keyboard, inline_choose_rate, inline_buy_rate
from utils.db_connection import create_table_user, \
    select_user, add_user, \
    make_reg, make_rate


bot = Bot(token=TOKEN)
storage = MemoryStorage()
disp = Dispatcher(bot=bot, storage=storage)


# класс состояния
class RegState(StatesGroup):
    user_id = State()
    start = State()
    chosen_rate = State()
    reg = State()
    pay_deposit = State()


'''
$$$$$$$$$$$$$$$
БАЗОВЫЕ ФУНКЦИИ
$$$$$$$$$$$$$$$
'''


async def check_reg_func(user_id: int):
    reg_status = select_user(tg_id=user_id)[2]
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


# функция при команде /start (приветствует и аннулирует всё, что было введено)
@disp.message_handler(commands='start', state='*')
@disp.message_handler(text='начать', state='*')
async def start_command(message: types.Message, state: FSMContext):
    await state.finish()

    user_id = message.from_user.id

    await RegState.user_id.set()
    await state.update_data(user_id=user_id)

    if not select_user(tg_id=user_id):
        add_user(tg_id=user_id, reg=False)

    await message.answer(
        text='''Привет!
Как я понимаю, ты хочешь получить доступ в мой ЗАКРЫТЫЙ ВИП КАНАЛ с сигналами для игры в LuckyJet?
Это БЕСПЛАТНО
За 1 неделю ты успеешь заработать на месячный доступ к моему ВИП КАНАЛУ.
Нужно сделать ряд простых условий и начать зарабатывать!''',
        reply_markup=main_keyboard
    )

    await RegState.start.set()

    await choose_rate(message=message, state=state)


# функция при команде /help (отправляет сообщение с ссылкой на личку)
@disp.message_handler(commands='help', state='*')
@disp.message_handler(text='помощь', state='*')
async def help_command(message: types.Message):
    await message.answer(
        text='''Тебе что-то не понятно или есть какие-то вопросы? Можешь обратиться <a href="https://t.me/strategvlad">сюда</a> 👇''',
        parse_mode='HTML',
    )


# функция при команде /check_reg (делает проверку регистрации)
@disp.message_handler(commands='check_reg', state='*')
@disp.message_handler(text='проверить регистрацию', state='*')
async def check_reg_command(message: types.Message):
    reg = await check_reg_func(user_id=message.from_user.id)

    if reg:
        await message.answer('Вы зарегистрированы!')
    else:
        await message.answer('''📲Для начала необходимо провести регистрацию на 1win (провайдер игры LuckyJet). Чтобы бот успешно проверил регистрацию, нужно соблюсти важные условия:

1️⃣Аккаунт обязательно должен быть НОВЫМ! Если у вас уже есть аккаунт и при нажатии на кнопку «РЕГИСТРАЦИЯ» вы попадаете на старый, необходимо выйти с него и заново нажать на кнопку «РЕГИСТРАЦИЯ», после чего по новой зарегистрироваться!

2️⃣Чтобы бот смог проверить вашу регистрацию, обязательно нужно ввести промокод bot22 при регистрации!''')


'''
$$$$$$$$$$$$$$$$$$$
ФУНКЦИИ РЕГИСТРАЦИИ
$$$$$$$$$$$$$$$$$$$
'''


# выбор тарифа
@disp.message_handler(state=RegState.start)
async def choose_rate(message: types.Message, state: FSMContext):
    await message.answer('Выбери тариф:', reply_markup=inline_choose_rate)

    await state.update_data(start=True)
    await RegState.chosen_rate.set()


@disp.callback_query_handler(state=RegState.chosen_rate, text=['always', 'month', 'free'])
async def chosen_rate(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    if call.message.text == 'always':
        await state.update_data(chosen_rate=2)
    elif call.message.text == 'month':
        await state.update_data(chosen_rate=1)
    elif call.message.text == 'free':
        await state.update_data(chosen_rate=0)

    await RegState.reg.set()

    reg_status = await check_reg_func(user_id=state_data["user_id"])
    if reg_status:
        await state.update_data(reg=True)
        await call.message.answer('Вы зарегистрированы!')

        await RegState.pay_deposit.set()
        await check_deposit(message=call.message, state=state)
    else:
        # await state.update_data(reg=False)
        await call.message.answer(text='''📲Для начала необходимо провести регистрацию на 1win (провайдер игры LuckyJet). Чтобы бот успешно проверил регистрацию, нужно соблюсти важные условия:

        1️⃣Аккаунт обязательно должен быть НОВЫМ! Если у вас уже есть аккаунт и при нажатии на кнопку «РЕГИСТРАЦИЯ» вы попадаете на старый, необходимо выйти с него и заново нажать на кнопку «РЕГИСТРАЦИЯ», после чего по новой зарегистрироваться!

        2️⃣Чтобы бот смог проверить вашу регистрацию, обязательно нужно ввести промокод CRYPA при регистрации!''')
        await make_reg_status(message=call.message, state=state)


@disp.message_handler(state=RegState.reg)
async def make_reg_status(message: types.Message, state: FSMContext):
    await message.answer('Ссылка на регистрацию...')
    await message.answer('Попробуйте начать заново! (нажмите /start)')

    await state.finish()


# проверка пополненного депозита
@disp.message_handler(state=RegState.pay_deposit)
async def check_deposit(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    paid_dep = await check_deposit_func(user_id=state_data["user_id"])

    if paid_dep:
        await message.answer(text='''Добро пожаловать в ВИП-чат! Вот ссылка на вход - https://t.me/+IwQ9bT41nzBiN2Yy
Если будут какие-то вопросы, то пиши мне @strategvlad''')
    else:
        await pay_deposit(message=message, state=state)


# пополнение депозита
@disp.message_handler(state=RegState.pay_deposit)
async def pay_deposit(message: types.Message, state: FSMContext):
    await message.answer(
        text='''!!️Для того, чтобы получить доступ в закрытую группу с сигналами, необходимо на любую сумму пополнить баланс аккаунта, который вы только что зарегистрировали.
На эти деньги вы будете делать ставки по сигналам.
Нажми на кнопку ПОПОЛНИТЬ ДЕПОЗИТ и тебе откроет 1WIN''',
        reply_markup=inline_buy_rate
    )

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(disp, skip_updates=True, on_startup=on_startup)
