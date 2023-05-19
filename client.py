from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from create_bot import dp, bot
from keyboards import keyboard
from data_base.kurer_db import cursor,base

async def select_all_types(message):
    inline_menu = types.InlineKeyboardMarkup()
    for res in cursor.execute('SELECT * FROM tagam_turleri').fetchall():
        btn = types.InlineKeyboardButton(text=res[1], callback_data=res[1])
        inline_menu.add(btn)
    await message.answer("Тағам түрлері. Бургерлер, Пиццалар, Сусындар 3-ке бөлінеді.", reply_markup=inline_menu)

async def select_tagamdar(message, id):
    for ret in cursor.execute(f"SELECT id, name,desc,price,photo FROM tagamdar WHERE type_id='{id}'").fetchall():
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="+", callback_data=str(ret[0])+"qosu")
        btn2 = types.InlineKeyboardButton(text="🗑", callback_data="sebetkeOtu")
        btn3 = types.InlineKeyboardButton(text="Сатып алу", callback_data="satypaly")
        kb.add(btn1,btn2).add(btn3)
        await message.answer_photo(ret[4],f"{ret[1]}\n{ret[2]}\n{ret[3]}",reply_markup=kb)

async def select_sebet(sebet,callback):
    d = {}
    for item in set(sebet):
        d[item] = sebet.count(item)
    for key in d:
        kb = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(text="Sebetten owiru", callback_data="sebettenOwiru")
        kb.add(btn2)
        res = cursor.execute(f"SELECT * FROM tagamdar WHERE id='{key}'").fetchall()[0]
        await callback.message.answer_photo(res[5],f"Аты:{res[2]},\nСипаттамасы️:{res[3]} {d[key]}\nБағасы:{res[4]}тг",reply_markup=kb)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Ботымызға қош келдіңіз! Біз сізді осында көргенімізге қуаныштымыз.Бұл жерде сіз мәзірдегі тағамды үйге тапсырыс бере аласыз")
    await message.answer('Бот 24/7 желіде жұмыс атқарады')
    await select_all_types(message)

@dp.message_handler(commands='Shygu')
async def add_command(message:types.Message):
    await message.answer("Sau bolynyz!🤗 \n Bizddin botta qaita kutemiz!:")

l = []
for el in cursor.execute('SELECT name FROM tagam_turleri').fetchall():
    l.append(el[0])

@dp.callback_query_handler()
async def print_tagam(callback:CallbackQuery):
    global l
    if callback.data in l:
        id = cursor.execute(f"SELECT id FROM tagam_turleri WHERE name='{callback.data}'").fetchall()[0][0]
        await select_tagamdar(callback.message, id)
        await callback.answer()
        await select_all_types(callback.message)
    elif "qosu" in callback.data:
        id = int(callback.data[0:callback.data.find("q")])
        cursor.execute(f'INSERT INTO sebet(tagam_id) values({id})')
        base.commit()
        print('sebetke qosyldy')
    elif callback.data == 'sebetkeOtu':
        sebet = []
        for el in cursor.execute('SELECT tagam_id FROM sebet').fetchall():
            sebet.append(el[0])
        await select_sebet(sebet, callback)
        await callback.message.answer("Себеттегі заттарыңызды сатып алу үшін\n/Сатыпалу\nкомандасын жазыныз ")
    elif callback.data == "sebettenOwiru":
        cursor.execute("DELETE FROM sebet")
        base.commit()
        await callback.answer("Себет тазаланды")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(add_command, commands='Shygu')
    dp.register_callback_query_handler(print_tagam)