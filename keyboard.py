from aiogram import types

add_menu = types.InlineKeyboardMarkup()
btn_tamak_kosu = types.InlineKeyboardButton(text="Тағам қосу", callback_data="tagamkosu")
btn_type_kosu = types.InlineKeyboardButton(text="Тағам түрін қосу", callback_data="typekosu")
add_menu.add(btn_tamak_kosu,btn_type_kosu)