import asyncio
import aioschedule
from datetime import datetime, timedelta
from random import choice

from aiogram.dispatcher import Dispatcher
from aiogram import Bot

from data.config import TOKEN
from utils.keyboard import inline_join_group, inline_buy_rate
from utils.db_connection import select_all_users


bot = Bot(token=TOKEN)
disp = Dispatcher(bot=bot)


async def scheduler():
    all_users = select_all_users()

    for user in all_users:
        now_datetime = datetime.now() - timedelta(hours=3)
        user_id = user[1]

        if not user[2]:
            # print('not reg')
            start_date = datetime.strptime(user[-1], '%Y-%m-%d %H:%M:%S')

            # ПРОВЕРКА НА ТО, ЧТО ПОЛЬЗОВАТЕЛЛЬ БОЛЕЕ 3 ДНЕЙ НЕ ЗАРЕГАН
            # if (((now_datetime - start_date).seconds // 60) % 2 == 1) and (((now_datetime - start_date).seconds // 60) != 1):
            if ((now_datetime - start_date).days % 2 == 1) and ((now_datetime - start_date).days != 1):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ

                random_choice = choice([0, 1])
                if random_choice == 0:
                    text = '''❗️Дружище, ты бы мог уже сегодня начать зарабатывать 💰, но до сих пор не прошёл регистрацию!
🔥Скорее жми кнопку НАЧАТЬ и получи инструкции! Регистрируйся и уже через 30 минут получишь свой первый сигнал ✅, который умножит твои деньги 🤑'''
                else:
                    text = '''❗️Уже через 30 минут дам последний сигнал ✅ в своей закрытой группе! Получить его может каждый из вас 😏 Надо всего лишь:
1️⃣ Нажми кнопку НАЧАТЬ и получи инструкции
2️⃣ Пройти регистрацию 😉
3️⃣ Получить доступ в закрытую группу 😎
4️⃣ Получить первый сигнал уже сегодня ✅'''
                await bot.send_message(
                    chat_id=user_id,
                    text=text,
                    reply_markup=inline_join_group
                )
                continue

        if user[3] is None and user[2]:
            # print('not pay')
            start_date = datetime.strptime(user[-3], '%Y-%m-%d %H:%M:%S')

            # ПРОВЕРКА НА ТО, ЧТО ПОЛЬЗОВАТЕЛЛЬ БОЛЕЕ 1 ДНЯ НЕ ПЛАТИТ ДЕПОЗИТ
            # if ((now_datetime - start_date).seconds // 60) >= 1:
            if (now_datetime - start_date).days >= 1:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ

                random_choice = choice([0, 1, 2])
                if random_choice == 0:
                    text = '''Когда ты готов начать зарабатывать? Мне важно показать тебе результат, ведь я работаю над масштабированием своей команды и мне важен каждый человек!
\nТы готов начать сегодня?
Тебе остался последний шаг, всего лишь оплатить депозит и начать зарабатывать!
Я для для этого тебе все инструменты!'''
                elif random_choice == 1:
                    text = '''Скоро начало игры по сигналам в моей ВИП группе!
Ты хочешь уже сегодня заработать свои первые деньги в онлайне не вставая с дивана?
Я жду тебя, тебе остался маленький шаг, для начала совместной работы со мной!'''
                else:
                    text = '''За неделю в среднем каждый мой подписчик зарабатывает +400% к своему депозиту!
Представь сколько ты бы смог зарабатывать не выходя их дома? Это фантастика!
Тебе остался всего один шаг для получения финансовой свободы!
Нажимай на кнопку ниже и давай начнем!'''

                await bot.send_message(
                    chat_id=user_id,
                    text=text,
                    reply_markup=inline_buy_rate
                )
                continue

    await bot.close()


async def main():
    aioschedule.every(1).day.do(scheduler)
    # aioschedule.every(1).minute.do(scheduler)

    while True:
        print('yo')
        await asyncio.create_task(aioschedule.run_pending())
        await asyncio.sleep(3600)
        # await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
