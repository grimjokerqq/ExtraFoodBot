from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token="6077416597:AAFR_1KT2sICfg2eJQTRGyucE-A831xFXLo")
dp = Dispatcher(bot,storage=storage)