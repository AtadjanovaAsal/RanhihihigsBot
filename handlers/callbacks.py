from aiogram.types import CallbackQuery
from db import async_session, add_user, user_exists
from .wordlist import mes_acc_created, mes_acc_already_exist

async def callback_continue(callback: CallbackQuery):
    """Ответ на кнопку продолжить"""

    async with async_session() as session:
        # Что-то проиходит
        await session.commit()
    await callback.message.answer("Успешно!")



async def callback_set_role(callback: CallbackQuery): # обработка выдачи статуса
    if await user_exists(callback.from_user.id): # проверка на регистрацию
        
        await callback.message.answer(mes_acc_already_exist) # отправляем сообщение
    else: # если пользователя нет в бд, просим зарегистрироваться
        data = callback.data # получаем дату
        status = data[5:] # делаем срез
        if await add_user(callback.from_user.id, callback.from_user.username, status):
            await callback.message.answer(mes_acc_created)
        else:
            await callback.message.answer(mes_acc_already_exist)