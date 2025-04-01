from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage


token = ''

bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())


