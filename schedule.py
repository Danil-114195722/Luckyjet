import asyncio

from datetime import datetime, timedelta

from aiogram.dispatcher import Dispatcher
from aiogram import Bot

from data.config import TOKEN
from utils.db_connection import select_all_users, del_rate
from data.constants import free_time, month_time, \
    push_not_reg_30min, push_not_reg_12hours, push_not_reg_4hours, push_not_reg_1day, push_not_reg_3days, push_not_reg_after_3days, \
    push_not_pay_1hour, push_not_pay_3hours, push_not_pay_12hours, push_not_pay_1day, push_not_pay_after_1day


bot = Bot(token=TOKEN)
disp = Dispatcher(bot=bot)


async def main():
    # while True:
    all_users = select_all_users()

    for user in all_users:
        now_datetime = datetime.now()
        user_id = user[1]

        if user[3] and user[3] != 2:
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
            start_date = datetime.strptime(user[-1], '%Y-%m-%d %H:%M:%S')
            # ПОСЫЛАЕМ ПУШИ БЕЗ РЕГИСТРАЦИИ

            # ЗДЕСЬ БУДЕТ ПРОВЕРКА НА ТО, ЧТО ПОЛЬЗОВАТЕЛЛЬ БОЛЕЕ 3 ДНЕЙ НЕ ЗАРЕГАН
            if now_datetime - start_date >= push_not_reg_3days:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 3days')
            elif now_datetime - start_date >= push_not_reg_1day:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 1day')
            elif now_datetime - start_date >= push_not_reg_12hours:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 12hours')
            elif now_datetime - start_date >= push_not_reg_4hours:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 4hours')
            elif now_datetime - start_date >= push_not_reg_30min:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_reg 30min')

        if not user[3] and user[2]:
            start_date = datetime.strptime(user[-1], '%Y-%m-%d %H:%M:%S')
            # ПОСЫЛАЕМ ПУШИ БЕЗ ОПЛАТЫ ДЕПОЗИТА

            # ЗДЕСЬ БУДЕТ ПРОВЕРКА НА ТО, ЧТО ПОЛЬЗОВАТЕЛЛЬ БОЛЕЕ 2 ДНЕЙ НЕ ПЛАТИТ ДЕПОЗИТ
            if now_datetime - start_date >= push_not_pay_1day:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay 1day')
            elif now_datetime - start_date >= push_not_pay_12hours:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay 12hours')
            elif now_datetime - start_date >= push_not_pay_3hours:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay 3hours')
            elif now_datetime - start_date >= push_not_pay_1hour:
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(chat_id=user_id, text='not_pay 1hour')

    await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
