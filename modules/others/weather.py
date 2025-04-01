import requests
import random
from bs4 import BeautifulSoup
from lxml import etree
from geopy.geocoders import Nominatim
from aiogram import Router, F,types
from bs4 import BeautifulSoup
from modules.others import proxy
from fake_useragent import UserAgent
from create_bot import bot
ua = UserAgent()
router = Router()

cfg_cloudly = {'Облачно с прояснениями':'⛅️',
               'Ясно': '☀️',
               'Пасмурно': '☁️',
               'Ливень': '🌧',
               'Небольшой дождь': '💦',
               'Дождь со снегом': '🌧❄️'
               }
timeout = 10


headers = {
    "User-Agent": ua.random
}
cookies = {'_ym_isad': '2', 'is_gdpr_b': 'CPHKBhCD+AE=', 'bh': 'EkwiTm90X0EgQnJhbmQiO3Y9IjgiLCJDaHJvbWl1bSI7dj0iMTIwIiwiWWFCcm93c2VyIjt2PSIyNC4xIiwiWW93c2VyIjt2PSIyLjUiGgUieDg2IiIMIjI0LjEuNS44MDMiKgI/MDoJIldpbmRvd3MiQgciNy4wLjAiSgQiNjQiUmQiTm90X0EgQnJhbmQiO3Y9IjguMC4wLjAiLCJDaHJvbWl1bSI7dj0iMTIwLjAuNjA5OS4yOTEiLCJZYUJyb3dzZXIiO3Y9IjI0LjEuNS44MDMiLCJZb3dzZXIiO3Y9IjIuNSIiWgI/MA==', 'is_gdpr': '0', '_ym_visorc': 'b', '_yasc': 'uGltsascFDEKW9zs3Hqb0KH9GdniqM42kU859bAmHMWyHwrRkUnIiyvnWLw5QvT7AA==', 'yashr': '1217990951713888337', '_ym_d': '1713888338', 'gdpr': '0', 'yabs-vdrf': 'A0', '_ym_uid': '1709839406178428189', 'cycada': 'RsZpUL4vLRWoIybmDE13RZcVLZSXmVyW1gBSQswFMLw=', 'i': 'TF4DWzPlHCGRB06k6jubDnN5NiTme6w5+5ObpnIQF6ecD3gHwCMANKnFT0Fwm45iRV8YquObsY4Tqt3XhnIu+YJmvKM=', 'yandexuid': '6182843831713888337', 'yp': '1713967129.uc.by#1713967129.duc.ru#1745424340.cld.2378379-1#2029248174.pcs.1#1714235225.szm.1:1920x1080:1881x939#1713895133.gpauto.52_093754:23_685102:100000:3:1713887933', 'yuidss': '6182843831713888337', 'ymex': '2029248339.yrts.1713888339'}

@router.message(F.text, lambda message: message.text.lower().split(' ')[0] == 'погода')
async def weather(message: types.Message):
    proxies = await get_proxy()
    city = message.text.lower().replace('погода ', '').strip()
    geolocator = Nominatim(user_agent=ua.random)
    location = geolocator.geocode(city)
    lat = location.latitude
    lon = location.longitude
    msg = await message.reply('🔎 Собираю информацию...')
    try:
        response = requests.get(url=f'https://yandex.by/pogoda/?lat={lat}&lon={lon}', headers=headers, proxies=proxies,
                                timeout=timeout, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        # текущая температура
        now_temp = soup.find(class_='temp fact__temp fact__temp_size_s').text
        # текущая облачность
        now_cloudly = soup.find(class_='link__condition day-anchor i-bem').text
        # текущая ощущение темпераутры
        now_temp_feel = soup.find(class_='term term_orient_h fact__feels-like').text
        # текущая скорость ветра
        now_wind_speed = soup.find(class_='term term_orient_v fact__wind-speed').find(class_='a11y-hidden').text
        # текущая влажность
        now_humidity = soup.find(class_='term term_orient_v fact__humidity').find(class_='a11y-hidden').text
        # текущее время
        now_time = soup.find(class_='fact__time-yesterday-wrap').find(class_='time fact__time').text
        try:
            # вчера в это время или другая инфа
            now_yesterday = soup.find(class_='term term_orient_h fact__yesterday').find(class_='a11y-hidden').text
        except:
            # вчера в это время или другая инфа
            now_yesterday = soup.find(
                class_='link link_theme_normal alert alert_level_blue alert_index_0 card anchor i-bem link_js_inited').find(
                class_='title-icon__text').text
        # осадки в ближайшее время
        now_precip = soup.find(class_='maps-widget-fact__title').text
        # прогноз погоды в ...
        title = soup.find('title').text.split('на')[0]

        await bot.edit_message_text(f'🔸 <b>{title}</b>\n'
                                    f'🔹 <i>{now_time} {now_yesterday}</i>\n\n'
                                    f'🌡 <b>Температура воздуха:</b> {now_temp}°\n'
                                    f'{await get_temp_feel(now_temp_feel)}°\n'
                                    f'☁️ <b>Облачность:</b> <i>{now_cloudly}</i> {cfg_cloudly[now_cloudly]}\n'
                                    f'{await get_wind_speed(now_wind_speed)}\n'
                                    f'{await get_humidity(now_humidity)}\n\n'
                                    f'<b>{now_precip}</b>', message.chat.id, msg.message_id, parse_mode='HTML')
    except Exception as e:
        print(e)
        await del_proxy(proxies['https'])
        await weather_try(message, msg.message_id)




async def weather_try(message: types.Message, edit_msg):
    proxies = await get_proxy()
    city = message.text.lower().replace('погода ', '').strip()
    geolocator = Nominatim(
        user_agent=ua.random)
    location = geolocator.geocode(city)
    lat = location.latitude
    lon = location.longitude
    try:
        response = requests.get(url=f'https://yandex.by/pogoda/?lat={lat}&lon={lon}', headers=headers, proxies=proxies, timeout=timeout, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        # текущая температура
        now_temp = soup.find(class_='temp fact__temp fact__temp_size_s').text
        # текущая облачность
        now_cloudly = soup.find(class_='link__condition day-anchor i-bem').text
        # текущая ощущение темпераутры
        now_temp_feel = soup.find(class_='term term_orient_h fact__feels-like').text
        # текущая скорость ветра
        now_wind_speed = soup.find(class_='term term_orient_v fact__wind-speed').find(class_='a11y-hidden').text
        # текущая влажность
        now_humidity = soup.find(class_='term term_orient_v fact__humidity').find(class_='a11y-hidden').text
        # текущее время
        now_time = soup.find(class_='fact__time-yesterday-wrap').find(class_='time fact__time').text
        try:
            # вчера в это время или другая инфа
            now_yesterday = soup.find(class_='term term_orient_h fact__yesterday').find(class_='a11y-hidden').text
        except:
            # вчера в это время или другая инфа
            now_yesterday = soup.find(
                class_='link link_theme_normal alert alert_level_blue alert_index_0 card anchor i-bem link_js_inited').find(
                class_='title-icon__text').text
        # осадки в ближайшее время
        now_precip = soup.find(class_='maps-widget-fact__title').text
        # прогноз погоды в ...
        title = soup.find('title').text.split('на')[0]

        await bot.edit_message_text(f'🔸 <b>{title}</b>\n'
                                    f'🔹 <i>{now_time} {now_yesterday}</i>\n\n'
                                    f'🌡 <b>Температура воздуха:</b> {now_temp}°\n'
                                    f'{await get_temp_feel(now_temp_feel)}°\n'
                                    f'☁️ <b>Облачность:</b> <i>{now_cloudly}</i> {cfg_cloudly[now_cloudly]}\n'
                                    f'{await get_wind_speed(now_wind_speed)}\n'
                                    f'{await get_humidity(now_humidity)}\n\n'
                                    f'<b>{now_precip}</b>', message.chat.id, edit_msg, parse_mode='HTML')
    except Exception as e:
        print(e)
        await del_proxy(proxies['https'])
        await weather_try(message, edit_msg)

async def get_proxy():
    with open('res/proxy/proxy_http.txt', 'r',encoding='utf-8') as f:
        lines = f.readlines()
        lines.pop(-1)
        proxy = str(random.choice(lines)).rstrip('\n')
        proxies = {
            'https': proxy
        }
        return proxies

async def del_proxy(proxy: str):
    with open('res/proxy/proxy_http.txt', 'r',encoding='utf-8') as f:
        lines = f.readlines()
        lines.pop(-1)
        lines.remove(proxy + '\n')
        with open('res/proxy/proxy_http.txt', 'w', encoding='utf-8') as f:
            f.writelines(lines)
async def get_temp_feel(now_temp_feel: str):
    if '−'in now_temp_feel:
        return f'🥶 <b>{now_temp_feel.split("−")[0]}:</b> -{now_temp_feel.split("−")[1]}'
    else:
        if int(now_temp_feel.split("+")[1]) > 10:
            return f'🥵 <b>{now_temp_feel.split("+")[0]}:</b> +{now_temp_feel.split("+")[1]}'
        else:
            return f'🥶 <b>{now_temp_feel.split("+")[0]}:</b> +{now_temp_feel.split("+")[1]}'

async def get_wind_speed(now_wind_speed: str):
    speed = now_wind_speed.split(': ')[1].split(',')[0]
    direction = now_wind_speed.split(': ')[1].split(',')[1]
    speed = speed.lower().replace('метров в секунду', 'м/с')
    return f'<b>💨 Ветер:</b> <i>{speed}, {direction}</i>'

async def get_humidity(now_humidity: str):
    text, humidity = now_humidity.split(' ')
    return f'💧 <b>{text}</b> <i>{humidity}</i>'
