import requests
from bs4 import BeautifulSoup
from time import perf_counter
import asyncio
import threading
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile
from fake_useragent import UserAgent
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}
router = Router()
@router.message(Command('proxy'))
async def send_proxy(message: types.Message):
    await message.reply_document(FSInputFile('res/proxy/proxy_http.txt'))



url = 'google.by'
end_list_proxies = []
# timeout проверки http(s)
timeout = 3
# количество потоков
count_threads = 50

def check_proxy_http(proxy: str):
    proxies = {'http': f'http://{proxy}'}
    try:
        response = requests.get('http://' + url, proxies=proxies, timeout=timeout)
        end_list_proxies.append(proxy)
    except Exception as e:
        pass

def get_http_proxy():
    list_http = []
    # github
    response = requests.get(f'https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt')
    list_http_p = response.text.replace('\r', '').split('\n')
    for i in list_http_p:
        if ':' in i:
            list_http.append(f'{i.split(":")[0]}:{i.split(":")[1]}')
    return list_http

def check_proxy_socks(proxy: str):
    proxies = {'https': proxy}
    try:
        start = perf_counter()
        response = requests.get(url='https://google.by', headers=headers, proxies=proxies, timeout=timeout)
        end = perf_counter()
        print(f'{proxy} - {round(end - start,3)}s')
        end_list_proxies.append(proxy)
    except Exception as e:
        pass

def get_socks_proxy():
    list_http = []
    # github

    response = requests.get(f'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt')
    list_socks4 = response.text.replace('\r', '').split('\n')
    response = requests.get(f'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt')
    list_socks5 = response.text.replace('\r', '').split('\n')
    for sock in list_socks4:
        list_http.append(f'socks4://{sock}')
    for sock in list_socks5:
        list_http.append(f'socks5://{sock}')
    #github
    response = requests.get(f'https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt')
    list_socks4 = response.text.replace('\r', '').split('\n')
    for sock in list_socks4:
        if ':' in sock:
            list_http.append(f'socks4://{sock.split(":")[0]}:{sock.split(":")[1]}')
    response = requests.get(f'https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt')
    list_socks5 = response.text.replace('\r', '').split('\n')
    for sock in list_socks5:
        if ':' in sock:
            list_http.append(f'socks5://{sock.split(":")[0]}:{sock.split(":")[1]}')
    #github
    response = requests.get(f'https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks4.txt')
    list_socks4 = response.text.replace('\r', '').split('\n')
    response = requests.get(f'https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks5.txt')
    list_socks5 = response.text.replace('\r', '').split('\n')
    for sock in list_socks4:
        list_http.append(f'socks4://{sock}')
    for sock in list_socks5:
        list_http.append(f'socks5://{sock}')
    return list_http


def get_proxy():
    start = perf_counter()

    list_proxies = get_socks_proxy()
    threads = []
    num = 0
    for proxy in list_proxies:
        threads.append(threading.Thread(target=check_proxy_socks, args=(proxy,)))
        num += 1
        if num == count_threads:
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
            num = 0
            threads.clear()
    end_list_proxies.append(f'Всего прокси: {len(end_list_proxies)}')
    with open('res/proxy/proxy_http.txt', 'w', encoding='utf-8') as f:
        f.writelines(prox + '\n' for prox in end_list_proxies)
    print(f'Кол-во пркоси:', len(end_list_proxies))
    end_list_proxies.clear()
    end = perf_counter()

