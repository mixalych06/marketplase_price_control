from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from dotenv import load_dotenv, find_dotenv
from data.bd import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv(find_dotenv(filename='.env'), encoding="utf-8", override=True)
TOKEN_BOT = os.environ.get('TOKEN')

db = DataBase('data/database.db')

bot: Bot = Bot(token=TOKEN_BOT)

dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
