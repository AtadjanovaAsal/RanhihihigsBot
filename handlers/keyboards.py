from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_continue = InlineKeyboardButton(
    text="Далле",
    callback_data="continue_button_pressed"
)

keyboard_continue = InlineKeyboardMarkup(inline_keyboard=[[button_continue]])



button_prepod = InlineKeyboardButton(text="Преподаватель", callback_data='role_prepod')
button_student = InlineKeyboardButton(text="Студент",  callback_data='role_student')


keyboard_roles = InlineKeyboardMarkup(inline_keyboard=[[button_prepod, button_student]])