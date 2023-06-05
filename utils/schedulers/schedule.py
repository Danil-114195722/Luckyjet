import asyncio
from datetime import datetime, timedelta
from random import choice

from aiogram.dispatcher import Dispatcher
from aiogram import Bot

from data.config import TOKEN
from utils.db_connection import select_all_users, del_rate
from utils.keyboard import inline_join_group, inline_buy_rate
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

            elif ((now_datetime - start_date) > (push_not_reg_1day - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_reg_1day):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(
                    chat_id=user_id,
                    text='''Еще раз привет! Ты уже надумал изменить свою жизнь и начать зарабатывать?
Ты уже долго думаешь и за это время мог бы уже заработать на хороший отдых на выходных с семьей!
Тебе не кажется, что пора менять свою жизнь?
Нажми кнопку НАЧАТЬ и получи инструкции!''',
                    reply_markup=inline_join_group
                )
                continue

            elif ((now_datetime - start_date) > (push_not_reg_12hours - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_reg_12hours):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(
                    chat_id=user_id,
                    text='''Ты думаешь уже целый рабочий день!
Обычный работяга за 12 часов (рабочую смену) зарабатывает 1.500 рублей и вечером падает в кровать без сил, а ты можешь не выходя из дома зарабатывать от 10.000 в день и кайфовать!
Ты хочешь так жить?
Нажми кнопку НАЧАТЬ и получи инструкции!''',
                    reply_markup=inline_join_group
                )
                continue

            elif ((now_datetime - start_date) > (push_not_reg_4hours - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_reg_4hours):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(
                    chat_id=user_id,
                    text='''Пока ты думаешь многие подписчики начали зарабатывать!
За 3 часа можно спокойно увеличить свой депозит в 2-3 раза!
Ты хочешь получить результаты уже сегодня?
Нажми кнопку НАЧАТЬ и получи инструкции!''',
                    reply_markup=inline_join_group
                )
                continue

            elif ((now_datetime - start_date) > (push_not_reg_30min - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_reg_30min):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(
                    chat_id=user_id,
                    text='''Друг, тебе надо все лишь зарегистрировать аккаунт, чтобы начать зарабатывать!
Это займет у тебя пару минут и ты сможешь начать зарабатывать уже сегодня!
Нажми кнопку НАЧАТЬ и получи инструкции!''',
                    reply_markup=inline_join_group
                )
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

            elif ((now_datetime - start_date) > (push_not_pay_12hours - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_pay_12hours):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(
                    chat_id=user_id,
                    text='''За рабочий день работяга на офисной работе зарабатывает 1.500 рублей, а ты мог бы увеличить свой депозит в 2-3 раза не выходя из дома!
Это прекрасная возможность жить полноценной жизнью!
Ты готов изменить свою жизнь?
Оплачивай депозит и я тебе дам доступ в ЗАКРЫТЫЙ ВИП КАНАЛ
Жми кнопку ниже!''',
                    reply_markup=inline_buy_rate
                )
                continue

            elif ((now_datetime - start_date) > (push_not_pay_3hours - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_pay_3hours):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(
                    chat_id=user_id,
                    text='''Только что прошла очередная игра и результаты феноменальные, отличные кафы и очень точные прогнозы на ставки!
Если играть уверено. по моей стратегии и сигналам, то можно каждый день стабильно зарабатывать от 40% к своему депозиту без нервов!
Ты готов начать? Тогда оплачивай депозит (нажми кнопку ниже), получай доступ в ВИП группу и начинай зарабатывать!''',
                    reply_markup=inline_buy_rate
                )
                continue

            elif ((now_datetime - start_date) > (push_not_pay_1hour - timedelta(minutes=1))) and \
                    ((now_datetime - start_date) <= push_not_pay_1hour):
                # ПОСЫЛАЕМ СООБЩЕНИЕ ЮЗЕРУ
                await bot.send_message(
                    chat_id=user_id,
                    text='''Приятель, только что прошла игра в моем ВИП канале и в среднем каждый участник ВИП группу увеличил свой депозит в 2 раза!
Почему ты все еще не присоединился к нам?
Оплачивай депозит и я тебе дам доступ в ЗАКРЫТЫЙ ВИП КАНАЛ
Жми кнопку ниже!''',
                    reply_markup=inline_buy_rate
                )
                continue

    await bot.close()


async def main():
    while True:
        await scheduler()
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
