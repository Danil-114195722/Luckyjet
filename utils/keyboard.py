from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

inline_join_group = InlineKeyboardMarkup(row_width=1)
inline_join_group.add(InlineKeyboardButton(text='НАЧАТЬ', callback_data='start'))

inline_buy_rate = InlineKeyboardMarkup(row_width=1)
# inline_buy_rate.add(InlineKeyboardButton(text='ПОПОЛНИТЬ ДЕПОЗИТ', callback_data='check_paid'))
inline_buy_rate.add(InlineKeyboardButton(text='ПОПОЛНИТЬ ДЕПОЗИТ', url='https://t.me/strategvlad'))
