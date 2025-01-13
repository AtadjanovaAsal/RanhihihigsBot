"""
import yadisk_async
import asyncio
async def test():
    Disk = yadisk_async.YaDisk(token='y0_AgAAAAA5BVBOAAzfxAAAAAEaqR2MAADc-DNn2kVIXrzmJ0VyCRvyjUaQJQ') # подключаемся к диску
    try:
        folder_data = [i async for i in (await Disk.listdir())] # пытаемся достать информацию о файлах в папке
    except:
        folder_data = None # если не получилось, ставим значение None
    if folder_data is None: # если файлов нет, то пропускаем папку
        pass
    else: # иначе начинаем проверку
        print('Sucs')
asyncio.run(test())
"""

from config import TOKEN
import asyncio  # асинхронный ввод-вывод
from aiogram import Bot, Dispatcher, types, filters
async def huita(botic):
    await botic.send_message(1749086960, 'Я@ТЫ@')
bot = Bot(TOKEN)
dp = Dispatcher()
asyncio.run(huita(bot))
