import aiogram.utils.exceptions

from create_bot import bot, db
from keyboards.user_keyboards import keyword

from aiogram import types
from aiogram.dispatcher import Dispatcher

from pars_wildberris import all_pars
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import choice

HELLO = f'🤖Я Телеграм-Бот!\nЯ могу отслеживать цены товаров на Wildberries.\nДля отслеживани отправьте мне сообщение с ссылкой на товар.\n' \
        f'Вы можете отправить мне до 5 ссылок' \
        f'💌Я сообщу вам если:\n' \
        f'   ❤цена уменьшится.\n' \
        f'   ❤товар удалён\n' \
        f'   ❤товар снова дотсупен по ссылке\n' \
        f'Ваши ранее загруженные ссылки можно посмотреть нажав на кнопку "🛍Мои товары"\n\n'


async def command_start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        await bot.send_photo(message.from_user.id, photo='https://setemonic.ru/wp-content/uploads/c/2/2/c221894c8c4cae57e76286f759e01e72.jpeg',
                             caption=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                                     f'{HELLO}<b>Нужно отслеживать больше товаров?</b>\n<b>Подключай 💎VIP💎</b>\n<i>Подробности у администратора '
                                     f'@mixalych06</i>',
                             parse_mode='HTML', reply_markup=keyword)
        db.add_user(message.from_user.id)
    else:
        await bot.send_photo(message.from_user.id, photo='https://setemonic.ru/wp-content/uploads/c/2/2/c221894c8c4cae57e76286f759e01e72.jpeg',
                             caption=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                                     f'{HELLO}<b>Нужно отслеживать больше товаров?</b>\n<b>Подключай 💎VIP💎</b>\n<i>Подробности у администратора '
                                     f'@mixalych06</i>',
                             parse_mode='HTML', reply_markup=keyword)


async def command_help(message: types.Message):
    await bot.send_photo(message.from_user.id, photo='https://setemonic.ru/wp-content/uploads/c/2/2/c221894c8c4cae57e76286f759e01e72.jpeg',
                         caption=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                                 f'{HELLO}<b>Нужно отслеживать больше товаров?</b>\n<b>Подключай 💎VIP💎</b>\n<i>Подробности у администратора '
                                 f'@mixalych06</i>',
                         parse_mode='HTML', reply_markup=keyword)


async def del_product(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split('|')
    db.del_product_bd((int(inline_command[1]), int(inline_command[2])))
    await callback_query.answer(text=f'{inline_command[3]}....\nОтслеживание цены прекращено.\n Обновите список нажмите\n🛍Мои товары',
                                show_alert=True)


async def user_product(message: types.Message):
    all_prod = db.all_product_in_user(message.from_user.id)
    if all_prod:
        for entries in all_prod:
            try:
                if entries[8] == 1:
                    await bot.send_photo(message.from_user.id, photo=entries[6],
                                         caption=f'<b>{entries[2]}</b>\n\n<b>Общая начальная цена:</b>  <i>{int(entries[3]) // 100} руб.</i>\n'
                                                 f'<b>Минимальная цена:</b>  <i>{int(entries[4]) // 100} руб.</i>\n'
                                                 f'<b>Текущая цена:</b>  <i>{int(entries[5]) // 100} руб.</i>\n{entries[7]}', parse_mode='HTML',
                                         reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                             'Не отслеживать', callback_data=f"del|{message.from_user.id}|{entries[1]}|{entries[2][:10]}")))
                else:
                    await bot.send_photo(message.from_user.id, photo=entries[6],
                                         caption=f'<b>{entries[2]}</b>\n\n<b>Общая начальная цена:</b>  <i>{int(entries[3]) // 100} руб.</i>\n'
                                                 f'<b>Минимальная цена:</b>  <i>{int(entries[4]) // 100} руб.</i>\n'
                                                 f'<b>Текущая цена:</b>  <i>Ссылка удалена</i>\n{entries[7]}', parse_mode='HTML',
                                         reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                             'Не отслеживать', callback_data=f"del|{message.from_user.id}|{entries[1]}|{entries[2][:10]}")))
            except aiogram.utils.exceptions.BadRequest:
                if entries[8] == 1:
                    await bot.send_photo(message.from_user.id, photo='https://cs.pikabu.ru/post_img/2013/04/06/6/1365237582_329952055.jpg',
                                         caption=f'Фото товара удалено или изменилось нажмите не кнопку не отслеживать, проверьте ссылку и '
                                                 f'отправьте мне её ещё раз '
                                                 f'<b>{entries[2]}</b>\n\n<b>Общая начальная цена:</b>  <i>{int(entries[3]) // 100} руб.</i>\n'
                                                 f'<b>Минимальная цена:</b>  <i>{int(entries[4]) // 100} руб.</i>\n'
                                                 f'<b>Текущая цена:</b>  <i>{int(entries[5]) // 100} руб.</i>\n{entries[7]}', parse_mode='HTML',
                                         reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                             'Не отслеживать', callback_data=f"del|{message.from_user.id}|{entries[1]}|{entries[2][:10]}")))
                else:
                    await bot.send_photo(message.from_user.id, photo='https://cs.pikabu.ru/post_img/2013/04/06/6/1365237582_329952055.jpg',
                                         caption=f'<b>{entries[2]}</b>\n\n<b>Общая начальная цена:</b>  <i>{int(entries[3]) // 100} руб.</i>\n'
                                                 f'<b>Минимальная цена:</b>  <i>{int(entries[4]) // 100} руб.</i>\n'
                                                 f'<b>Текущая цена:</b>  <i>Ссылка удалена</i>\n{entries[7]}', parse_mode='HTML',
                                         reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                             'Не отслеживать', callback_data=f"del|{message.from_user.id}|{entries[1]}|{entries[2][:10]}")))
                continue
    else:
        await message.answer('У вас нет сохранённых ссылок')


async def echo_send(message: types.Message):
    e = message.text
    all_prod = db.all_product_in_user(message.from_user.id)
    if 'wildberries.ru' in e and 'detail.aspx' in e:
        try:
            x = all_pars(e)
            print(x)
        except TypeError:
            await message.reply('Не полная ссылка')
            return
        if db.select_user_prod(message.from_user.id, x['id']):
            await message.reply(choice(['🤖Эта ссылка уже отслеживается', '🤖Я уже слежу для Вас за этим товаром',
                                        '🤖Ссылка была добавлена ранее, я обязательно сообщу Вам об уменьшении цены']))
            return

        elif db.vip_user_exists(message.from_user.id):
            vip_user = db.vip_user(message.from_user.id)
            if vip_user[1] - len(all_prod) >= 0:
                await bot.send_photo(message.from_user.id, photo=x['link_photo'],
                                     caption=f'<b>{x["name"]}</b>\n\n<b>Общая начальная цена:</b>  <i>{x["salePriceU"] // 100} руб.</i>\n'
                                             f'<b>Минимальная цена:</b>  <i>{x["salePriceU"] // 100} руб.</i>\n'
                                             f'<b>Текущая цена:</b>  <i>{x["salePriceU"] // 100} руб.\n{x["link"]}</i>', reply_markup=keyword,
                                     parse_mode='HTML')
                db.add_product(message.from_user.id, x)
                return
            else:
                await message.reply(f'🤖Для вас я могу отследить до {vip_user[1]} ссылок одновременно.\n'
                                    'Пожалуйста удалите ненужные ссылки или свяжитесь с администратором бота для увеличения количества')
                return

        elif all_prod and len(all_prod) > 4:
            await message.reply('🤖Я не умею отслеживать 🔦 более 5 ссылок одновременно.\n'
                                'Удалите ненужные ссылки.\n<b>Хотите отслеживать больше товаров?</b>\n<b>Подключай 💎VIP💎</b>\n<i>Подробности у '
                                'администратора @mixalych06</i>', parse_mode='HTML')
            return
        else:
            await bot.send_photo(message.from_user.id, photo=x['link_photo'],
                                 caption=f'<b>{x["name"]}</b>\n\n<b>Общая начальная цена:</b>  <i>{x["salePriceU"] // 100} руб.</i>\n'
                                         f'<b>Минимальная цена:</b>  <i>{x["salePriceU"] // 100} руб.</i>\n'
                                         f'<b>Текущая цена:</b>  <i>{x["salePriceU"] // 100} руб.\n{x["link"]}</i>', reply_markup=keyword,
                                 parse_mode='HTML')
            db.add_product(message.from_user.id, x)
            return
    elif e.startswith('https://www.wildberries.ru') and not ('detail.aspx' in e):
        await message.reply('Не полная ссылка')
        return
    elif 'https://www.ozon.ru' in e:
        await message.reply('Это ссылка на Озон, я пока не научился с ним работать.')
        return
    else:
        await message.answer(choice(['Когда нибудь я научусь понимать человеческий язык и мы с вами обязательно поговорим.', 'Я вас не понимаю',
                                     'Э-ЭХ, мне бы ссылочку на Wildberries']))
        return


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(del_product, lambda x: x.data.startswith('del'))
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_help, text=['🆘Помощь'])
    dp.register_message_handler(user_product, text=['🛍Мои товары'])
    dp.register_message_handler(echo_send)
