import requests
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}




def get_location(url):
    with open('proxy_http.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        proxies = {
            'https': line
        }
        response = requests.get(url=url, headers=headers, proxies=proxies, verify=False)
        soup = BeautifulSoup(response.text, 'lxml')

        ip = soup.find('div', class_='ip').text.strip()
        location = soup.find('div', class_='value-country').text.strip()

        print(f'IP: {ip.rstrip()}\nLocation: {location.rstrip()}')


def main():
    get_location(url='https://2ip.ru')

main()
