import asyncio
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
            # print('yo2')
            start_date = datetime.strptime(user[-1], '%Y-%m-%d %H:%M:%S')
            # ПОСЫЛАЕМ ПУШИ БЕЗ РЕГИСТРАЦИИ

            if ((now_datetime - start_date) > (push_not_reg_3days - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_reg_3days):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 3days')
                continue

            elif ((now_datetime - start_date) > (push_not_reg_1day - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_reg_1day):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 1day')
                continue

            elif ((now_datetime - start_date) > (push_not_reg_12hours - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_reg_12hours):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 12hours')
                continue

            elif ((now_datetime - start_date) > (push_not_reg_4hours - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_reg_4hours):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 4hours')
                continue

            elif ((now_datetime - start_date) > (push_not_reg_30min - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_reg_30min):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 30min')
                continue
            else:
                continue

        if user[2] and user[3] is None:
            # print('yo1')
            start_date = datetime.strptime(user[-3], '%Y-%m-%d %H:%M:%S')
            # ПОСЫЛАЕМ ПУШИ БЕЗ ОПЛАТЫ ДЕПОЗИТА

            if ((now_datetime - start_date) > (push_not_pay_1day - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_pay_1day):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay 1day')
                continue

            elif ((now_datetime - start_date) > (push_not_pay_12hours - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_pay_12hours):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                print(f'not_pay 12hours {user_id} {now_datetime - start_date}')
                await bot.send_message(chat_id=user_id, text='not_pay 12hours')
                continue

            elif ((now_datetime - start_date) > (push_not_pay_3hours - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_pay_3hours):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                print(f'not_pay 3hours {user_id} {now_datetime - start_date}')
                await bot.send_message(chat_id=user_id, text='not_pay 3hours')
                continue

            elif ((now_datetime - start_date) > (push_not_pay_1hour - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_pay_1hour):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                print(f'not_pay 1hour {user_id} {now_datetime - start_date}')
                await bot.send_message(chat_id=user_id, text='not_pay 1hour')
                continue

    await bot.close()


async def main():
    while True:
        await scheduler()
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
