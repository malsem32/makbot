import asyncio
import logging
import threading

from aiogram import types, F
from aiogram.filters import Command, CommandObject

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import config
import database
from create_bot import bot
from create_bot import dp
from database import db_data
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pytz
from datetime import datetime
from aiogram.types.input_file import FSInputFile

#  Логгирование
logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w')


@dp.message(Command('logs'))
async def send_logs(message: types.message):
    user_id = message.from_user.id
    if user_id in config.admin_id:
        await message.reply_document(open('app/logs.log', 'rb'))
    else:
        await message.reply('Облом =)')


# /me Пасспорт
@dp.message(Command('me'))
async def mce(message: types.Message):
    await database.check_user(message.from_user.id, message.from_user.username)
    user_id = message.from_user.id
    user_info = db_data.users.find_one({'user_id': user_id})
    img = Image.open(f'res/profile_pic/pattern.png').convert("RGBA")
    font = ImageFont.truetype(f'res/fonts/Arimo-SemiBold.ttf', size=40)
    draw_text = ImageDraw.Draw(img)
    # работа
    draw_text.text((155, 325),
                   str(user_info["job"]),
                   font=font,
                   fill=213)
    # деньги
    draw_text.text((155, 269),
                   str(await num_triadi(user_info["cash"])),
                   font=font,
                   fill=213)
    # крипта
    draw_text.text((155, 377),
                   str(0),
                   font=font,
                   fill=213)
    # Гражданство
    if user_info['citizen_country'] == 'нет':
        draw_text.text((155, 445),
                       'Беженец',
                       font=font,
                       fill='#0D0D0D')
    elif user_info['citizen_country'] != 'нет' and user_info['president_country'] == 'нет':
        draw_text.text((155, 445),
                       user_info['citizen_country'],
                       font=font,
                       fill='#0D0D0D')
    elif user_info['citizen_country'] != 'нет' and user_info['president_country'] != 'нет':
        draw_text.text((155, 445),
                       f'{user_info["citizen_country"]}, президент',
                       font=font,
                       fill='#0D0D0D')
    # дата
    tz = pytz.timezone('Etc/GMT-3')
    time_now = f'{f"0{datetime.now(tz=tz).day}" if len(str(datetime.now(tz=tz).day)) == 1 else datetime.now(tz=tz).day}.{f"0{datetime.now(tz=tz).month}" if len(str(datetime.now(tz=tz).month)) == 1 else datetime.now(tz=tz).month}.{datetime.now(tz=tz).year}\n{datetime.now(tz=tz).hour}:{f"0{datetime.now(tz=tz).minute}" if len(str(datetime.now(tz=tz).minute)) == 1 else datetime.now(tz=tz).minute}'
    font_time = ImageFont.truetype(f'res/fonts/Arimo-SemiBold.ttf', size=24)
    draw_text.text((820, 446),
                   time_now,
                   font=font_time,
                   fill=15)
    # фото профиля
    user_profile_photo = await bot.get_user_profile_photos(message.from_user.id, limit=1)
    if user_profile_photo.photos:
        file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
        await bot.download_file(file.file_path, f'res/profile_pic/cache/profile.png')
        img_profile = Image.open(f'res/profile_pic/cache/profile.png').convert("RGBA")
        # создание круга
        size = (180, 180)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(img_profile, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save(f'res/profile_pic/cache/profile2.png')

        img_profile2 = Image.open(f'res/profile_pic/cache/profile2.png').convert("RGBA")
        img.alpha_composite(img_profile2, (100, 60))
    # Если нет аватарки
    else:
        img_profile = Image.open(f'res/profile_pic/default_avatar.png').convert("RGBA")
        # создание круга
        size = (180, 180)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(img_profile, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save(f'res/profile_pic/cache/profile2.png')

        img_profile2 = Image.open(f'res/profile_pic/cache/profile2.png').convert("RGBA")
        img.alpha_composite(img_profile2, (100, 60))
    # Имя
    draw_text.text((300, 90),
                   message.from_user.first_name,
                   font=font,
                   fill=213)
    # ID
    font_id = ImageFont.truetype(f'res/fonts/Arimo-SemiBold.ttf', size=25)
    draw_text.text((300, 140),
                   f'ID: {message.from_user.id}',
                   font=font_id,
                   fill=213)
    img.save(f'res/profile_pic/cache/me.png')
    await bot.send_photo(message.chat.id, photo=FSInputFile(f'res/profile_pic/cache/me.png'))


# Паспорт
@dp.message(F.text, lambda message: message.text.lower() in ['я', 'паспорт', 'профиль', 'мой профиль', 'баланс'])
async def me_text(message: types.Message):
    await get_username_from_id(message.from_user.id)
    await mce(message)

@dp.message(Command('tag'))
async def tagg(message: types.Message, command: CommandObject):
    args: str = command.args
    await message.reply(await username_2(args, 'пользователь'), parse_mode='HTML')
async def username_2(user_id, username):
    id_name = await bot.get_chat(user_id)
    return f'<a href="tg://user?id={user_id}">{id_name.username}</a>'
# разбитие на триады
async def num_triadi(num):
    return "{:,}".format(num).replace(",", " ")


# Вызывается при старте
async def on_startup():
    print('Бот ЕБАШИТ')
    await bot.send_message(config.admin_id[0], 'Я работаю!')


async def get_username_from_id(user_id: int):
    id_name = await bot.get_chat(user_id)
    if id_name.username is None:
        return id_name.first_name
    else:
        return id_name.username
#scheduler = AsyncIOScheduler()
#scheduler.start()

async def main() -> None:
    #from modules.others.schedulers import start_schedulers
    #start_schedulers()
    dp.startup.register(on_startup)
    #from modules.reg_modules import reg_routers
    #reg_routers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())


