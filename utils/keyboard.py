from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


main_keyboard = InlineKeyboardMarkup(row_width=1)
main_keyboard.add(InlineKeyboardButton(text='РЕГИСТРАЦИЯ', url='https://1wmgzr.top/?open=register&'))
main_keyboard.add(InlineKeyboardButton(text='ПРОВЕРИТЬ РЕГИСТРАЦИЮ', callback_data='check_reg'))
main_keyboard.add(InlineKeyboardButton(text='ПОМОЩЬ', url='https://t.me/strategvlad'))

inline_choose_rate = InlineKeyboardMarkup(row_width=1)
inline_choose_rate.add(InlineKeyboardButton(text='Навсегда (70к)', url='http://24time2pay.ru/pay-id90.html', callback_data='always'))
inline_choose_rate.add(InlineKeyboardButton(text='На месяц (25к)', url='http://24time2pay.ru/pay-id90.html', callback_data='month'))
inline_choose_rate.add(InlineKeyboardButton(text='На неделю (БЕСПЛАТНО)', callback_data='free'))

inline_join_group = InlineKeyboardMarkup(row_width=1)
inline_join_group.add(InlineKeyboardButton(text='НАЧАТЬ', callback_data='start'))

inline_buy_rate = InlineKeyboardMarkup(row_width=1)
inline_buy_rate.add(InlineKeyboardButton(text='ПОПОЛНИТЬ ДЕПОЗИТ', url='https://r47fss.ru/', callback_data='check_paid'))
