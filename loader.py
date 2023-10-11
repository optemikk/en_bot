from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from database import Database

storage = MemoryStorage()
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=storage)
database = Database()