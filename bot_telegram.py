from aiogram.utils import executor
from create_bot import dp
from data_base import kurer_db
from handlers import admin, client

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True)