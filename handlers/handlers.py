# -- Обработчики (handlers) --
# Все обработчики должны быть подключены к маршрутизатору (или диспетчеру)
# Обработчики (handlers) — обработчик сообщений, который будет возвращать другое сообщение, указанное в функции

__all__ = [
    "register_message_handler"
]

# Установить общий уровень логирования и создали экземпляр лога
import logging
from aiogram import Router, types, filters, F
from db import (user_exists,
                add_user,
                add_ref,
                add_path,
                get_status,
                get_role,
                get_token,
                set_token,
                rem_path,
                )
from sqlalchemy import select, insert
from .keyboards import keyboard_roles
from .callbacks import callback_set_role
from .wordlist import *
from .yandex import check_token, check_path
import asyncio

# справочная информация


# настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



async def command_help_handler(message: types.Message) -> None:
    """Команда справки /help"""
    await message.answer(help_string)
        
async def command_start_handler(message: types.Message) -> None:
    """Команда регистрации/start"""

    if await user_exists(message.from_user.id):
        message.answer(mes_acc_already_exist)
    else:
        start_command = message.text
        if len(start_command) > 7:
            refferer_id = str(start_command[7:])
        else:
            refferer_id = None
        if await add_ref(message.from_user.id, refferer_id):
            await message.answer(mes_choose_role, reply_markup=keyboard_roles)
        else:
            await message.answer(mes_acc_already_exist)

async def command_status_handler(message: types.Message) -> None:
    """Команда информации о пользователе /status"""
    
    info = await get_status(message.from_user.id)
    if info:
        await message.answer(info, parse_mode="HTML")
    else:
        await message.answer(mes_no_user)
    logger.info(f"user {message.from_user.id} asks for status!")
    
async def command_register_handler(message: types.Message) -> None:
    if await user_exists(message.from_user.id):
        if await get_role(message.from_user.id) == 'student':
            await message.answer(mes_not_for_us)
        else:
            data = message.text.split()
            if len(data) == 1:
                await message.answer(mes_setup_init)
                await asyncio.sleep(0.5)
                await message.answer(mes_setup_first)
                await asyncio.sleep(0.5)
                await message.answer(mes_setup_second)
                await asyncio.sleep(0.5)
                await message.answer(mes_setup_third)
                await asyncio.sleep(0.5)
                await message.answer(mes_setup_last)
                await asyncio.sleep(0.5)
            elif len(data) == 2:
                await message.answer(f"{mes_token_link}{data[1].strip()}")
            else:
                await message.answer(mes_unexp_err)
    else:
        await message.answer(mes_no_user)
                
async def command_token_handler(message: types.Message) -> None:
    if await user_exists(message.from_user.id):
        if await get_role(message.from_user.id) == 'student':
            await message.answer(mes_not_for_us)
        else:
            data = message.text.split()
            if len(data) == 1:
                await message.answer(mes_no_token)
            elif len(data) == 2:
                if check_token(data[1].strip()):
                    if await set_token(message.from_user.id, data[1].strip()):
                        await message.answer(mes_token_set)
                    else:
                        await message.answer(mes_token_err)
                else:
                    await message.answer(mes_token_err)
            else:
                await message.answer(mes_unexp_err)
    else:
        await message.answer(mes_no_user)
        
async def command_add_handler(message: types.Message) -> None:
    if await user_exists(message.from_user.id):
        if await get_role(message.from_user.id) == 'student':
            await message.answer(mes_not_for_us)
        else:
            data = message.text
            if len(data) < 5:
                await message.answer(mes_no_path)
            else:
                token = await get_token(message.from_user.id)
                print (token)
                if await check_token(token):
                    path = data[5:] if data[-1] == '/' else data[5:] + '/'
                    if await check_path(token, path):
                        if await add_path(message.from_user.id, path):
                            await message.answer(mes_path_added)
                        else:
                            await message.answer(mes_path_err)
                    else:
                        await message.answer(mes_path_err)
                else:
                    await message.answer(mes_token_err)
    else:
        await message.answer(mes_no_user)
                
async def command_delete_handler(message: types.Message) -> None:
    if await user_exists(message.from_user.id):
        if await get_role(message.from_user.id) == 'student':
            await message.answer(mes_not_for_us)
        else:
            data = message.text
            if len(data) < 8:
                await message.answer(mes_no_path)
            else:
                token = await get_token(message.from_user.id)
                if await check_token(token):
                    path = data[8:] if data[-1] == '/' else data[8:] + '/'
                    if await check_path(token, path):
                        if await rem_path(message.from_user.id, path):
                            await message.answer(mes_path_deleted)
                        else:
                            await message.answer(mes_path_err)
                    else:
                        await message.answer(mes_path_err)
                else:
                    await message.answer(mes_token_err)
    else:
        await message.answer(mes_no_user)

async def process_unknown_command(message: types.Message) -> None:
    """эхо-ответ"""
    await message.reply(text="Неподдерживаемая команда. Введите /help для справки.")
    logger.info(f"user {message.from_user.id} send unknown message or command!")


async def register_message_handler(router: Router):
    """Маршрутизация"""
    router.message.register(command_help_handler, filters.Command(commands=["help"]))
    router.message.register(command_start_handler, filters.Command(commands=["start"]))
    router.message.register(command_status_handler, filters.Command(commands=["status"]))
    router.message.register(command_register_handler, filters.Command(commands=["register"]))
    router.message.register(command_token_handler, filters.Command(commands=["token"]))
    router.message.register(command_add_handler, filters.Command(commands=["add"]))
    router.message.register(command_delete_handler, filters.Command(commands=["delete"]))
    router.callback_query.register(callback_set_role, F.data.startswith("role_"))
    router.message.register(process_unknown_command)