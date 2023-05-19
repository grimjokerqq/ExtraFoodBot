from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
import random
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.dispatcher.filters import Text
from data_base.kurer_db import cursor,base
from keyboards.keyboard import add_menu
from handlers.client import select_all_types,select_tagamdar

class AddAdmin(StatesGroup):
    waiting_for_password = State()

admins = ['user_id_1', 'user_id_2']

admin1_password = '23018898'
admin2_password = '23018678'

async def insert_tagam(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO tagamdar(type_id,name,desc,price,photo) values(?,?,?,?,?)",tuple(data.values()))
    base.commit()
    print('database ok')

class adminFSM(StatesGroup):
    tagam_type_name = State()
    tagam_type_id = State()
    tagam_name = State()
    tagam_desc = State()
    tagam_price = State()
    tagam_photo = State()

class addresFSM(StatesGroup):
    address = State()

class kurerFSM(StatesGroup):
    photo = State()
    name = State()

@dp.message_handler(commands='add')
async def add_command(message:types.Message):
    if str(message.from_user.id) in admins:
        await message.answer('Вы уже являетесь администратором.')
    else:
        await message.answer('Ozgeris engizu ushin qupiasoz engiz!:')
        await AddAdmin.waiting_for_password.set()

@dp.message_handler(state=AddAdmin.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    if message.text == admin1_password or message.text == admin2_password :
        admins.append(str(message.from_user.id))
        await message.answer('Admin boldynyz quttiktaimyz.')
        await message.answer("Ne qosqynyz keledi?:", reply_markup=add_menu)
    else:
        await message.answer('Qate terdiniz,qaita koriniz.')
    await state.finish()

@dp.callback_query_handler(Text(equals='typekosu'))
async def type_kosu(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer("Тағамның атын енгіз:")
    await state.set_state(adminFSM.tagam_type_name)
    await callback.answer()

@dp.message_handler(state=adminFSM.tagam_type_name)
async def load_type(message:types.Message,state:FSMContext):
    print(message.text)
    cursor.execute(f"INSERT INTO tagam_turleri(name) values('{message.text}')")
    base.commit()
    print('database ok')
    await state.finish()

@dp.callback_query_handler(Text(equals='tagamkosu'))
async def tagam_kosu(callback:CallbackQuery, state:FSMContext):
    await select_all_types(callback.message)
    await state.set_state(adminFSM.tagam_type_id)
    await callback.answer()

@dp.message_handler(state=adminFSM.tagam_type_id)
async def load_tagam_id(message:types.Message,state:FSMContext):
    id = cursor.execute(f"SELECT id FROM tagam_turleri WHERE name='{message.text}'").fetchall()[0][0]
    async with state.proxy() as data:
        data['id'] = id
    await state.set_state(adminFSM.tagam_name)
    await message.answer("Tagam atayin engiz:")

@dp.message_handler(state=adminFSM.tagam_name)
async def load_tagam_name(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await state.set_state(adminFSM.tagam_desc)
    await message.answer("Tagam sipatyn engiz:")

@dp.message_handler(state=adminFSM.tagam_desc)
async def load_tagam_desc(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await state.set_state(adminFSM.tagam_price)
    await message.answer("Tagam bagasyn engiz:")

@dp.message_handler(state=adminFSM.tagam_price)
async def load_tagam_price(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['price'] = int(message.text)
    await state.set_state(adminFSM.tagam_photo)
    await message.answer("Suretin engiz:")

@dp.message_handler(state=adminFSM.tagam_photo, content_types=['photo'])
async def load_tagam_photo(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await insert_tagam(state)
    await state.finish()
    await message.answer("Rakmet")


@dp.message_handler(commands=['Сатыпалу'])
async def track_order(message:types.Message):
    total_price = cursor.execute(f"SELECT SUM(tagamdar.price) FROM sebet INNER JOIN tagamdar ON tagamdar.id=sebet.tagam_id").fetchone()[0]
    await message.answer(f"Сіз {total_price} суммасына тапсырыс бердіңіз\nмекенжайыңызды жазып жіберіңіз.")
    await addresFSM.address.set()

@dp.message_handler(state=addresFSM.address)
async def get_address(message:types.Message, state: FSMContext):
    list = ['Айбек','Дидар','Сәулетбек']
    address = message.text
    await state.finish()
    await message.answer(f"Рахмет тапсырысыңыз қабылданды. Біз оны : '{address}' қа {random.randint(15,30)} минутта курьер жеткізеді.\nКурьердың аты {random.choice(list)}")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(add_command, commands='add')
    dp.register_message_handler(process_password, state=AddAdmin.waiting_for_password)
    dp.register_callback_query_handler(type_kosu, Text(equals='typekosu'))
    dp.register_message_handler(load_type, state=adminFSM.tagam_type_name)
    dp.register_callback_query_handler(tagam_kosu, Text(equals='tagamkosu'))
    dp.register_message_handler(load_tagam_id, state=adminFSM.tagam_type_id)
    dp.register_message_handler(load_tagam_name, state=adminFSM.tagam_name)
    dp.register_message_handler(load_tagam_desc, state=adminFSM.tagam_desc)
    dp.register_message_handler(load_tagam_price, state=adminFSM.tagam_price)
    dp.register_message_handler(load_tagam_photo, state=adminFSM.tagam_photo, content_types=['photo'])
    dp.register_message_handler(track_order, commands=['Сатып алу'])
    dp.register_message_handler(get_address, state=addresFSM.address)