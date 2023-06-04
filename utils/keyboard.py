from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


main_buttons = ['начать', 'проверить регистрацию', 'помощь']
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton(main_buttons[0]), KeyboardButton(main_buttons[1]))
main_keyboard.add(KeyboardButton(main_buttons[2]))

inline_choose_rate = InlineKeyboardMarkup(row_width=1)
inline_choose_rate.add(InlineKeyboardButton(text='Навсегда (70к)', callback_data='always'))
inline_choose_rate.add(InlineKeyboardButton(text='На месяц (25к)', callback_data='month'))
inline_choose_rate.add(InlineKeyboardButton(text='На неделю (бесплатно)', callback_data='free'))

inline_buy_rate = InlineKeyboardMarkup(row_width=1)
inline_buy_rate.add(InlineKeyboardButton(text='ПОПОЛНИТЬ ДЕПОЗИТ', url='https://r47fss.ru/'))
