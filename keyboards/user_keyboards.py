from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyword: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

button_user_link: KeyboardButton = KeyboardButton('🛍Мои товары')
button_help: KeyboardButton = KeyboardButton('🆘Помощь')
keyword.add(button_user_link, button_help)
