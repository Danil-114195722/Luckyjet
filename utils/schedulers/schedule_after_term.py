import asyncio
from time import sleep
from datetime import datetime, timedelta
import aioschedule

from aiogram.dispatcher import Dispatcher
from aiogram import Bot

from data.config import TOKEN
from utils.db_connection import select_all_users


bot = Bot(token=TOKEN)
disp = Dispatcher(bot=bot)


async def scheduler():
    all_users = select_all_users()

    for user in all_users:
        now_datetime = datetime.now() - timedelta(hours=3)
        user_id = user[1]

        if not user[2]:
            print('not reg')
            start_date = datetime.strptime(user[-1], '%Y-%m-%d %H:%M:%S')
            # ПОСЫЛАЕМ ПУШИ БЕЗ РЕГИСТРАЦИИ

            # ЗДЕСЬ БУДЕТ ПРОВЕРКА НА ТО, ЧТО ПОЛЬЗОВАТЕЛЛЬ БОЛЕЕ 3 ДНЕЙ НЕ ЗАРЕГАН
            # if (now_datetime - start_date).days % 2 == 1 and (now_datetime - start_date).days != 1:
            if (now_datetime - start_date).seconds % 2 == 1 and (now_datetime - start_date).seconds != 1:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg more 3days')

        if user[3] is None and user[2]:
            print('not pay')
            start_date = datetime.strptime(user[-3], '%Y-%m-%d %H:%M:%S')

            # ЗДЕСЬ БУДЕТ ПРОВЕРКА НА ТО, ЧТО ПОЛЬЗОВАТЕЛЛЬ БОЛЕЕ 1 ДНЯ НЕ ПЛАТИТ ДЕПОЗИТ
            # if (now_datetime - start_date).days >= 1:
            if (now_datetime - start_date).seconds >= 1:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay more 1day')

    await bot.close()


async def main():
    aioschedule.every(1).day.do(scheduler)

    while True:
        print('yo')
        await asyncio.create_task(aioschedule.run_pending())
        await asyncio.sleep(3600)


if __name__ == '__main__':
    asyncio.run(main())
