
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import math
from aiogram.filters import Command
from aiogram import types, Router, F
from database import db_data
from create_bot import bot
from PIL import Image, ImageDraw, ImageFont, ImageOps
from aiogram.types.input_file import FSInputFile
from datetime import datetime
import pytz
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.input_media_photo import InputMediaPhoto
import json
router = Router()

# Страны /countries
@router.message(Command('countries'))
async def countries(message: types.Message):
    countries_info = list(db_data.countries.find())
    res_page = float(len(countries_info)) / 5
    msg = []
    for country in countries_info:
        num = countries_info.index(country)
        if num == 5:
            break
        else:
            with open('res/json/countries.json', 'r', encoding='utf-8') as f:
                json_countries = json.load(f)
                count_name = country["country"]
            msg.append(f'<i>{num+1}. {json_countries[count_name]} {country["country"]} \n</i>'
                       f'🤵‍♂️ <b>Президент:</b> {"Без президента" if country["president"] == "нет" else await get_url_tag(country["president"])}\n'
                       f'💵 <b>Стоимость:</b> {await num_triadi(country["cost"]) } $\n'
                       f'🌐 <b>Территория:</b> {await num_triadi(country["territory"])} км²\n'
                       f'🔸 <b>Уровень:</b> {country["level"]}\n\n')
    msg.append(f'<code>Страница 1 из {math.ceil(res_page)}</code>')
    key = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔙', callback_data='countries_back_1'),InlineKeyboardButton(text='🛒 Купить', callback_data='buy_country') ,InlineKeyboardButton(text='🔜', callback_data='countries_soon_2')]
    ])
    await message.reply(''.join(msg), parse_mode='HTML', disable_notification=True, reply_markup=key)

# Страны
@router.message(F.text, lambda message: message.text.lower() == 'страны')
async def countries_t(message: types.Message):
    await countries(message)
# Вперед список
@router.callback_query(lambda callback: 'countries_soon_' in callback.data)
async def countries_back(callback: types.CallbackQuery):

    page = int(callback.data.replace('countries_soon_',''))
    countries_info = list(db_data.countries.find())
    res_page = float(len(countries_info)) / 5
    if math.ceil(res_page) + 1  == page:
        await callback.answer('Это уже последняя страница!')
    else:
        num_start_country = page*5-5
        num_end_country = page*5
        msg = []
        num = 1
        for item in range(num_start_country,num_end_country):
            try:
                country = countries_info[item]
                count_name = country["country"]
                msg.append(f'<i>{num}. {get_flag(count_name)} {country["country"]}\n</i>'
                           f'🤵‍♂️ <b>Президент:</b> {"Без президента" if country["president"] == "нет" else await get_url_tag(country["president"])}\n'
                           f'💵 <b>Стоимость:</b> {await num_triadi(country["cost"])} $\n'
                           f'🌐 <b>Территория:</b> {await num_triadi(country["territory"])} км²\n'
                           f'🔸 <b>Уровень:</b> {country["level"]}\n\n')
                num+=1
            except IndexError:
                break
        msg.append(f'<code>Страница {page} из {math.ceil(res_page)}</code>')
        key = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔙', callback_data=f'countries_back_{page-1}'),
             InlineKeyboardButton(text='🛒 Купить', callback_data='buy_country'),
             InlineKeyboardButton(text='🔜', callback_data=f'countries_soon_{page+1}')]
        ])
        await callback.message.edit_text(''.join(msg), parse_mode='HTML', disable_notification=True, reply_markup=key)
# Назад список
@router.callback_query(lambda callback: 'countries_back_' in callback.data)
async def countries_back(callback: types.CallbackQuery):
    page = int(callback.data.replace('countries_back_',''))
    countries_info = list(db_data.countries.find())
    res_page = float(len(countries_info)) / 5
    if page == 0:
        await callback.answer('Это уже последняя страница!')
    else:
        num_start_country = page*5-5
        num_end_country = page*5
        msg = []
        num = 1
        for item in range(num_start_country,num_end_country):
            countries_info = list(db_data.countries.find())
            country = countries_info[item]
            count_name = country["country"]
            msg.append(f'<i>{num}. {get_flag(count_name)} {country["country"]}\n</i>'
                   f'🤵‍♂️ <b>Президент:</b> {"Без президента" if country["president"] == "нет" else await get_url_tag(country["president"])}\n'
                   f'💵 <b>Стоимость:</b> {await num_triadi(country["cost"])} $\n'
                   f'🌐 <b>Территория:</b> {await num_triadi(country["territory"])} км²\n'
                   f'🔸 <b>Уровень:</b> {country["level"]}\n\n')
            num+=1
        msg.append(f'<code>Страница {page} из {math.ceil(res_page)}</code>')
        key = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔙', callback_data=f'countries_back_{page-1}'),
             InlineKeyboardButton(text='🛒 Купить', callback_data='buy_country'),
             InlineKeyboardButton(text='🔜', callback_data=f'countries_soon_{page+1}')]
        ])
        await callback.message.edit_text(''.join(msg), parse_mode='HTML', disable_notification=True, reply_markup=key)
# Удалить
@router.callback_query(lambda callback: 'del_msg' == callback.data)
async def del_msg(callback: types.CallbackQuery):
    await callback.message.delete()
# Список стран для покупки
@router.callback_query(lambda callback: callback.data == 'buy_country')
async def buy_country(callback: types.CallbackQuery):
    country_list = list(db_data.countries.find({'president': 'нет'}))
    key = InlineKeyboardBuilder()
    for country in country_list:
        country = country["country"]
        key.add(InlineKeyboardButton(text=f'{get_flag(country)} {country}', callback_data=f'buy_country_{country}'))
    key.adjust(3)
    key.row(InlineKeyboardButton(text='Назад', callback_data='country_back'),width=1)
    await callback.message.edit_text('Страны доступные к покупке:',reply_markup=key.as_markup())

# Назда кнопка
@router.callback_query(lambda callback: 'country_back' == callback.data)
async def c_back(callback: types.CallbackQuery):
    countries_info = list(db_data.countries.find())
    res_page = float(len(countries_info)) / 5
    msg = []
    for country in countries_info:
        num = countries_info.index(country)
        if num == 5:
            break
        else:
            with open('res/json/countries.json', 'r', encoding='utf-8') as f:
                json_countries = json.load(f)
                count_name = country["country"]
            msg.append(f'<i>{num + 1}. {json_countries[count_name]} {country["country"]} \n</i>'
                       f'🤵‍♂️ <b>Президент:</b> {"Без президента" if country["president"] == "нет" else await get_url_tag(country["president"])}\n'
                       f'💵 <b>Стоимость:</b> {await num_triadi(country["cost"])} $\n'
                       f'🌐 <b>Территория:</b> {await num_triadi(country["territory"])} км²\n'
                       f'🔸 <b>Уровень:</b> {country["level"]}\n\n')
    msg.append(f'<code>Страница 1 из {math.ceil(res_page)}</code>')
    key = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔙', callback_data='countries_back_1'),
         InlineKeyboardButton(text='🛒 Купить', callback_data='buy_country'),
         InlineKeyboardButton(text='🔜', callback_data='countries_soon_2')]
    ])
    await callback.message.edit_text(''.join(msg), parse_mode='HTML', disable_notification=True, reply_markup=key)
# Купить страну
@router.callback_query(lambda callback: 'buy_country_' in callback.data)
async def buy_country_c(callback: types.CallbackQuery):
    user_info = db_data.users.find_one({'user_id': callback.from_user.id})
    if user_info['president_country'] != 'нет':
        await callback.answer(f'У вас уже есть страна: {user_info["president_country"]}')
    else:
        country = callback.data.split('_')[-1].capitalize()
        country_info = db_data.countries.find_one({'country': country})
        if country_info is not None:
            if country_info['president'] == 'нет':
                if user_info['cash'] >= country_info['cost']:
                    await callback.message.delete()
                    citizens = list(db_data.users.find({'citizen_country': country}))
                    # Вычет денег из баланса
                    db_data.users.update_one({'user_id':callback.from_user.id},
                                              {'$set': {'cash': user_info['cash'] - country_info['cost'],
                                                        'president_country': country,
                                                        'citizen_country': country}})
                    # Страна обрела президента
                    db_data.countries.update_one({'country': country}, {'$set': {'president': callback.from_user.id}})

                    img = Image.open(f'res/country_pic/pattern.png').convert("RGBA")
                    font = ImageFont.truetype(f'res/fonts/Blogger_Sans.otf', size=60)
                    draw_text = ImageDraw.Draw(img)
                    # Президент
                    draw_text.text((200, 975),
                                   str(callback.from_user.username if callback.from_user.username is not None else callback.from_user.first_name),
                                   font=font,
                                   fill='#F6D0C7')
                    # Казна
                    draw_text.text((200, 1117),
                                   f'{await num_triadi(country_info["cash"])} $',
                                   font=font,
                                   fill='#F6D0C7')
                    # НАсление
                    draw_text.text((200, 1259),
                                   f'{len(citizens)} из {country_info["max_people"]}',
                                   font=font,
                                   fill='#F6D0C7')
                    # Уровень
                    draw_text.text((200, 1401),
                                   f'{country_info["level"]}',
                                   font=font,
                                   fill='#F6D0C7')
                    # Название страны
                    draw_text.text((200, 1694),
                                   str(country_info["country"]),
                                   font=font,
                                   fill='#100404')
                    # Время
                    tz = pytz.timezone('Etc/GMT-3')
                    time_now = f'{f"0{datetime.now(tz=tz).day}" if len(str(datetime.now(tz=tz).day)) == 1 else datetime.now(tz=tz).day}.{f"0{datetime.now(tz=tz).month}" if len(str(datetime.now(tz=tz).month)) == 1 else datetime.now(tz=tz).month}.{datetime.now(tz=tz).year}\n{datetime.now(tz=tz).hour}:{f"0{datetime.now(tz=tz).minute}" if len(str(datetime.now(tz=tz).minute)) == 1 else datetime.now(tz=tz).minute}'
                    font_time = ImageFont.truetype(f'res/fonts/Blogger_Sans.otf', size=42)
                    draw_text.text((785, 1680),
                                   time_now,
                                   font=font_time,
                                   fill='#100404')
                    # Флаг
                    img_flag = Image.open(f'res/country_pic/{country_info["country"]}.png').convert(
                        "RGBA")
                    new_img_flag = img_flag.resize((884, 470))
                    img.paste(new_img_flag, (92, 300))

                    img.save(f'res/country_pic/cache/img.png')
                    await bot.send_photo(callback.from_user.id,photo=FSInputFile(f'res/country_pic/cache/img.png'), parse_mode='HTML')
            else:
                await callback.answer('Данная страна уже имеет президента!')

# О стране
@router.message(Command('mycountry'))
async def my_Country(message: types.Message):
    user_info = db_data.users.find_one({'user_id': message.from_user.id})
    if user_info['president_country'] == 'нет':
        await message.reply(f'У вас нет страны!\n'
                            f'❗️ Чтобы посмотреть список стран введите:<i> Страны</i>', parse_mode='HTML')
    else:
        country_info = db_data.countries.find_one({'country': user_info['president_country']})
        citizens = list(db_data.users.find({'citizen_country': user_info['president_country']}))
        img = Image.open(f'res/country_pic/pattern.png').convert("RGBA")
        font = ImageFont.truetype(f'res/fonts/Blogger_Sans.otf', size=60)
        draw_text = ImageDraw.Draw(img)
        # Президент
        draw_text.text((200, 975),
                       str(message.from_user.username if message.from_user.username is not None else message.from_user.first_name),
                       font=font,
                       fill='#F6D0C7')
        # Казна
        draw_text.text((200, 1117),
                       f'{await num_triadi(country_info["cash"])} $',
                       font=font,
                       fill='#F6D0C7')
        # НАсление
        draw_text.text((200, 1259),
                       f'{len(citizens)} из {country_info["max_people"]}',
                       font=font,
                       fill='#F6D0C7')
        # Уровень
        draw_text.text((200, 1401),
                       f'{country_info["level"]}',
                       font=font,
                       fill='#F6D0C7')
        # Название страны
        draw_text.text((200, 1690),
                       str(country_info["country"]),
                       font=font,
                       fill='#100404')
        # Время
        tz = pytz.timezone('Etc/GMT-3')
        time_now = f'{f"0{datetime.now(tz=tz).day}" if len(str(datetime.now(tz=tz).day)) == 1 else datetime.now(tz=tz).day}.{f"0{datetime.now(tz=tz).month}" if len(str(datetime.now(tz=tz).month)) == 1 else datetime.now(tz=tz).month}.{datetime.now(tz=tz).year}\n{datetime.now(tz=tz).hour}:{f"0{datetime.now(tz=tz).minute}" if len(str(datetime.now(tz=tz).minute)) == 1 else datetime.now(tz=tz).minute}'
        font_time = ImageFont.truetype(f'res/fonts/Blogger_Sans.otf', size=42)
        draw_text.text((785, 1680),
                       time_now,
                       font=font_time,
                       fill='#100404')
        # Флаг
        img_flag = Image.open(f'res/country_pic/{country_info["country"]}.png').convert(
            "RGBA")
        new_img_flag = img_flag.resize((884, 470))
        img.paste(new_img_flag, (92, 300))

        img.save(f'res/country_pic/cache/img.png')
        await message.reply_photo(photo=FSInputFile(f'res/country_pic/cache/img.png'), parse_mode='HTML')

# О стране
@router.message(F.text, lambda message: message.text.lower() in ['о стране','моя страна', 'страна'])
async def my_country_text(message:types.Message):
    await my_Country(message)

# Продать страну
@router.message(Command('sell_country'))
async def sell_country(message: types.Message):
    country_name = db_data.users.find_one({'user_id': message.from_user.id})
    if country_name['president_country'] != 'нет':
        country_info = db_data.countries.find_one({'country': country_name['president_country']})
        key = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Да', callback_data=f'sell_country_yes_{message.from_user.id}'),
             InlineKeyboardButton(text='Нет', callback_data=f'sell_country_no_{message.from_user.id}')]
        ])
        await message.reply(f'Вы хотите продать страну {country_info["country"]} за {int(float(country_info["cost"])/2)} $ ?', reply_markup=key)
    else:
        await message.reply('У вас нет страны!')



def get_flag(country_name: str):
    with open('res/json/countries.json', 'r', encoding='utf-8') as f:
        json_countries = json.load(f)
        return json_countries[country_name]

# разбитие на триады
async def num_triadi(num):
    return "{:,}".format(num).replace(",", " ")

# Ссылка пользоваетля в тег
async def get_url_tag(user_id: int):
    id_name = await bot.get_chat(user_id)
    if id_name.username is None:
        return f'<a href="tg://user?id={user_id}">{id_name.first_name}</a>'
    else:
        return f'<a href="tg://user?id={user_id}">{id_name.username}</a>'