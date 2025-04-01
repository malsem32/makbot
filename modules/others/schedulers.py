from bot import scheduler
from modules.others.proxy import get_proxy
import asyncio
import pytz
from datetime import datetime, timedelta
def start_schedulers():
    # Поиск прокси при запуске
    tz = pytz.timezone('Etc/GMT-3')
    time_now = datetime.now(tz=tz)+timedelta(seconds=5)
    scheduler.add_job(get_proxy, 'date', run_date=time_now)

    # Поиск прокси каждые 10 минут
    scheduler.add_job(get_proxy,'interval', minutes=10)