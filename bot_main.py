from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pars_wildberris import all_pars, parsing_evry_day
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from random import choice
from data.bd import DataBase
from time import sleep
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


bot: Bot = Bot(os.getenv('TOKEN'))
dp: Dispatcher = Dispatcher(bot)
keyword: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

db = DataBase('data/database.db')
button_user_link: KeyboardButton = KeyboardButton('🛍Мои товары')
button_help: KeyboardButton = KeyboardButton('🆘Помощь')
keyword.add(button_user_link, button_help)

HELLO = f'Я Телеграм-Бот!🤖\nЯ могу отслеживать цены товаров на Wildberries.\nДля отслеживани отправьте мне сообщение с ссылкой на товар.\n' \
        f'Если цена уменьшится, я сообщу Вам.\n'\
        f'Ваши ранее загруженные ссылки можно посмотреть нажав на кнопку "Мои товары")'


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        await bot.send_photo(message.from_user.id, photo='https://setemonic.ru/wp-content/uploads/c/2/2/c221894c8c4cae57e76286f759e01e72.jpeg',
                             caption=f'Привет, {message.from_user.first_name}!\n{HELLO}', reply_markup=keyword)
        db.add_user(message.from_user.id)
    else:
        await bot.send_photo(message.from_user.id, photo='https://setemonic.ru/wp-content/uploads/c/2/2/c221894c8c4cae57e76286f759e01e72.jpeg',
                             caption=f'Привет, {message.from_user.first_name}!\n{HELLO}', reply_markup=keyword)


@dp.message_handler(text='🆘Помощь')
async def command_help(message: types.Message):
    await bot.send_photo(message.from_user.id, photo='https://setemonic.ru/wp-content/uploads/c/2/2/c221894c8c4cae57e76286f759e01e72.jpeg',
                         caption=f'Привет, {message.from_user.first_name}!\n{HELLO}', reply_markup=keyword)

@dp.callback_query_handler(lambda x: x.data.startswith('del'))
async def del_product(callback_query: types.CallbackQuery):
    inlaine_command = callback_query.data.split('|')
    db.del_product_bd((int(inlaine_command[1]), int(inlaine_command[2])))
    await callback_query.answer(text=f'{inlaine_command[3]}....\nОтслеживание цены прекращено.\n Обновите список нажмите\n🛍Мои товары', show_alert=True)



@dp.message_handler(text='🛍Мои товары')
async def user_product(message: types.Message):
    all_prod = db.all_product_in_user(message.from_user.id)
    if all_prod:
        for entries in all_prod:
            await bot.send_photo(message.from_user.id, photo=entries[6],
                                 caption=f'<b>{entries[2]}</b>\n\n<b>Общая начальная цена:</b>  <i>{int(entries[3])//100} руб.</i>\n'
                                         f'<b>Минимальная цена:</b>  <i>{int(entries[4])//100} руб.</i>\n'
                                         f'<b>Текущая цена:</b>  <i>{int(entries[5])//100} руб.</i>\n{entries[7]}', parse_mode='HTML',
                                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                     'Не отслеживать',callback_data=f"del|{message.from_user.id}|{entries[1]}|{entries[2][:10]}")))
    else:
        await message.answer('У вас нет сохранённых ссылок')




@dp.message_handler()
async def echo_send(message: types.Message):
    e = message.text
    if e.startswith('https://www.wildberries.ru') and 'detail.aspx' in e:
        x = all_pars(e)
        if db.select_user_prod(message.from_user.id, x['id']):
            await message.reply(choice(['Эта ссылка уже отслеживается', 'Я уже слежу для Вас за этим товаром',
                                     'Ссылка была добавлена ранее, я обязательно сообщу Вам об уменьшении цены']))
            return
        # elif
        else:
            await bot.send_photo(message.from_user.id, photo=x['link_photo'],
                                 caption=f'<b>{x["name"]}</b>\n\n<b>Общая начальная цена:</b>  <i>{x["salePriceU"] // 100} руб.</i>\n'
                                         f'<b>Минимальная цена:</b>  <i>{x["salePriceU"] // 100} руб.</i>\n'
                                         f'<b>Текущая цена:</b>  <i>{x["salePriceU"] // 100} руб.\n{x["link"]}</i>', reply_markup=keyword, parse_mode='HTML')
            db.add_product(message.from_user.id, x)
            return
    elif e.startswith('https://www.wildberries.ru') and not ('detail.aspx' in e):
        await message.reply('Не полная ссылка')
        return
    elif e.startswith('https://www.ozon.ru'):
        await message.reply('Это ссылка на Озон, я пока не научился с ним работать.')
        return
    else:
        await message.answer(choice(['Когда нибудь я научусь понимать человеческий язык и мы с вами обязательно поговорим.', 'Я вас не понимаю',
                                     'Э-ЭХ, мне бы ссылочку на Wildberries']))
        return


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        users_list = db.select_users()
        for user in users_list:
            user_prod = db.all_product_in_user(user[0])
            if user_prod:
                for prod in user_prod:
                    new_pars_produkt = parsing_evry_day(prod[7])
                    try:
                        if new_pars_produkt['salePriceU'] < prod[3] and new_pars_produkt['salePriceU'] < prod[4]:
                            '''шлём сообщение о снижении ценыб перезаписываем минималку и текущую'''
                            await bot.send_message(user[0], text=f'{prod[2]}\nЦена снижена.\nМеньше начальной цены на '
                                                                 f'{int(100 - ((new_pars_produkt["salePriceU"]//100) * 100 / (int(prod[3])//100)))}%\n'
                                                                 f'Цена минимальная🤑 с момента отслеживания.')
                            db.changes_product_data((new_pars_produkt['salePriceU'], new_pars_produkt['salePriceU'], prod[0], prod[1]))
                            sleep(1)
                            continue

                        elif new_pars_produkt['salePriceU'] < prod[5] and new_pars_produkt['salePriceU'] >= prod[4] and new_pars_produkt['salePriceU'] < prod[3]:
                            '''сообщение о снижении, перезаписываем текущую'''
                            await bot.send_message(user[0], text=f'{prod[2]}\nЦена снижена.\nМеньше начальной цены на'
                                                                 f'{int(100 - ((new_pars_produkt["salePriceU"] // 100) * 100 / (int(prod[3]) // 100)))}%\n')
                            db.changes_product_data((prod[4], new_pars_produkt['salePriceU'], prod[0], prod[1]))
                            sleep(1)
                            continue

                        else:
                            db.changes_product_data((prod[4], new_pars_produkt['salePriceU'], prod[0], prod[1]))
                            await bot.send_message(user[0], text=f'{prod[2]}\nЦена не изменилась')
                    except:
                        db.off_user(prod[0])
                        print('меня заблокировали')
            else:

                continue


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10800))
    executor.start_polling(dp, skip_updates=True)
