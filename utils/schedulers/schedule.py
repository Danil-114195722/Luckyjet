import asyncio

from time import sleep
from datetime import datetime, timedelta

from aiogram.dispatcher import Dispatcher
from aiogram import Bot

from data.config import TOKEN
from utils.db_connection import select_all_users, del_rate
from data.constants import free_time, month_time, \
    push_not_reg_30min, push_not_reg_12hours, push_not_reg_4hours, push_not_reg_1day, push_not_reg_3days, \
    push_not_pay_1hour, push_not_pay_3hours, push_not_pay_12hours, push_not_pay_1day


bot = Bot(token=TOKEN)
disp = Dispatcher(bot=bot)


async def scheduler():
    all_users = select_all_users()
    print(all_users)
    for user in all_users:
        now_datetime = datetime.now() - timedelta(hours=3)
        user_id = user[1]

        if user[3] is not None and user[3] != 2:
            rate_date = datetime.strptime(user[-2], '%Y-%m-%d %H:%M:%S')

            if user[3] == 1:
                if now_datetime - rate_date >= month_time:
                    # АННУЛИРУЕМ ОПЛАТУ
                    del_rate(tg_id=user_id)

            elif user[3] == 0:
                if now_datetime - rate_date >= free_time:
                    # АННУЛИРУЕМ ОПЛАТУ
                    del_rate(tg_id=user_id)

        if not user[2]:
            print('yo2')
            start_date = datetime.strptime(user[-1], '%Y-%m-%d %H:%M:%S')
            print(now_datetime)
            print(start_date)
            # ПОСЫЛАЕМ ПУШИ БЕЗ РЕГИСТРАЦИИ

            if now_datetime.day == (start_date + push_not_reg_3days).day:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 3days')
                continue

            elif now_datetime.day == (start_date + push_not_reg_1day).day:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 1day')
                continue

            elif now_datetime.hour == (start_date + push_not_reg_12hours).hour:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 12hours')
                continue

            # elif now_datetime.hour == (start_date + push_not_reg_4hours).hour:
            elif now_datetime.minute == (start_date + push_not_reg_4hours).minute:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                print('not_reg 4hours')
                await bot.send_message(chat_id=user_id, text='not_reg 4hours')
                continue

            elif now_datetime.minute == (start_date + push_not_reg_30min).minute:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                print('not_reg 30min')
                await bot.send_message(chat_id=user_id, text='not_reg 30min')
                continue

        if user[3] is None and user[2]:
            print('yo1')
            start_date = datetime.strptime(user[-3], '%Y-%m-%d %H:%M:%S')
            print(now_datetime)
            print(start_date)
            # ПОСЫЛАЕМ ПУШИ БЕЗ ОПЛАТЫ ДЕПОЗИТА

            if now_datetime.day == (start_date + push_not_pay_1day).day:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay 1day')
                continue

            elif now_datetime.hour == (start_date + push_not_pay_12hours).hour:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay 12hours')
                continue

            # elif now_datetime.hour == (start_date + push_not_pay_3hours).hour:
            elif now_datetime.minute == (start_date + push_not_pay_3hours).minute:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay 3hours')
                continue

            # elif now_datetime.hour == (start_date + push_not_pay_1hour).hour:
            elif now_datetime.minute == (start_date + push_not_pay_1hour).minute:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay 1hour')
                continue

    await bot.close()


async def main():
    while True:
        await scheduler()
        sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
