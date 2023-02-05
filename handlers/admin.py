from aiogram import types
from create_bot import db
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.admin_keyboards import keyword_root_user, keyword_admin
from keyboards.user_keyboards import keyword

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(filename='.env'), encoding="utf-8", override=True)
ROOT_U = int(os.environ.get('ROOT_USER'))


class FSMRoot(StatesGroup):
    id_admin = State()
    del_id_admin = State()


'''Добавление админа'''


async def cm_start(message: types.Message):
    await FSMRoot.id_admin.set()
    await message.reply('Введите id')


async def load_id(message: types.Message, state: FSMContext):
    if db.su_user_exists(int(message.text)):
        await message.answer(f'Пользователь {message.text} уже является администратором.')
        await state.finish()
    else:
        async with state.proxy() as data:
            data['id_admin'] = message.text
        db.add_su_user(int(data['id_admin']))
        await message.answer(f'Пользователь {data["id_admin"]} добавлен.')
        await state.finish()


'''Удаление админа'''


async def cm_del(message: types.Message):
    await FSMRoot.del_id_admin.set()
    await message.reply('Введите id для удаления')


async def del_id_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_admin'] = message.text
    db.del_su_user_bd(int(data['id_admin']))
    await message.answer(f'Пользователь {data["id_admin"]} удалён.')
    await state.finish()


async def command_start_admin(message: types.Message):
    if message.from_user.id == ROOT_U:
        await message.answer('Привет, Создатель!', reply_markup=keyword_root_user)
        return
    elif db.su_user_exists(message.from_user.id):
        await message.answer(f'Привет, {message.from_user.first_name}!\nВы в меню администратора бота', reply_markup=keyword_admin)
        return
    else:
        await message.answer('Вы не являетесь администратором.', reply_markup=keyword)


async def user_id(message: types.Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')


async def command_how_many_users(message: types.Message):
    if message.from_user.id == ROOT_U:
        await message.answer(f'Активных пользователей: {len(db.select_users())}\n'
                             f'Не активных пользователей: {len(db.select_off_users())}')
        return
    elif db.su_user_exists(message.from_user.id):
        await message.answer(f'Активных пользователей: {len(db.select_users())}\n'
                             f'Не активных пользователей: {len(db.select_off_users())}')
        return
    else:
        await message.answer('Вы не являетесь администратором.', reply_markup=keyword)


async def add_admin(message: types.Message):
    print(message.values)
    if message.from_user.id == ROOT_U:
        print(message.values)
        db.add_su_user(int(''.join([i for i in message.text if i.isdigit()])))
        await message.answer('Пользователь добавлен.', reply_markup=keyword_root_user)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, text=['Добавить админа'], state=None)
    dp.register_message_handler(load_id, state=FSMRoot.id_admin)
    dp.register_message_handler(cm_del, text=['Удалить админа'], state=None)
    dp.register_message_handler(del_id_admin, state=FSMRoot.del_id_admin)
    dp.register_message_handler(command_start_admin, commands=['start_admin'])
    dp.register_message_handler(command_how_many_users, text=['Пользователей в базе'])
    dp.register_message_handler(user_id, commands=['user_ID'])
