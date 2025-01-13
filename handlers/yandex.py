
import yadisk_async
from aiogram import Bot
from  db import get_folders, get_token, get_refs, set_date
from datetime import datetime
import asyncio


async def check_token(token):
    Disk = yadisk_async.YaDisk(token=token)
    try:
        res = await Disk.check_token()
        return res
        await Disk.close()
    except:
        await Disk.close()
        return None
        
        
async def check_path(token, path):
    Disk = yadisk_async.YaDisk(token=token)
    try:
        if [i async for i in await Disk.listdir(f"disk:{path}")]:
            return True
    except:
        await Disk.close()
        return False
        
        
async def check_new_files(bot_token) -> None:
    bot = Bot(bot_token)
    while True:
        await asyncio.sleep(90)
        folders = await get_folders()
        for i in folders:
            user_id = int(i[0].user_id)
            token = await get_token(user_id)
            Disk = yadisk_async.YaDisk(token=token)
            try:
                folder_data = [i async for i in (await Disk.listdir(f"disk:{i[0].folder_path}"))]
                for f in folder_data: # берём файлы последовательно
                    if f['file'] is None: # если это папка, то пропускаем
                        pass
                    else:
                        if f['modified'].timestamp() > i[0].check_date.timestamp():
                            refs = await get_refs(user_id)
                            for ref in refs:
                                await bot.send_message(ref[0].user_id, text = f"Файл {f['name']} обновлен {f['modified']}")
            except:
                pass
            await set_date(i[0].id, datetime.now())
            await asyncio.sleep(1)
            await Disk.close()