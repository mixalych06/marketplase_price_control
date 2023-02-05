from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyword_root_user: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
keyword_admin: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

button_how_many_users: KeyboardButton = KeyboardButton('Пользователей в базе')
button_add_admin: KeyboardButton = KeyboardButton('Добавить админа')
button_del_admin: KeyboardButton = KeyboardButton('Удалить админа')
button_help: KeyboardButton = KeyboardButton('🆘Помощь')
keyword_root_user.add(button_how_many_users).add(button_add_admin, button_del_admin).add(button_help)
keyword_admin.add(button_how_many_users).add(button_help)

