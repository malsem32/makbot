from pymongo import MongoClient

db_data = MongoClient(
    "").data

cfg_games = MongoClient(
    "").cfg

from datetime import datetime
import pytz


async def check_user(user_id: int, username: str):
    tz = pytz.timezone('Etc/GMT-3')
    user = db_data.users.find_one({'user_id': user_id})
    if user is None:
        db_data.users.insert_one({'user_id': user_id,
                                  'cash': 0,
                                  'president_country': 'нет',
                                  'citizen_country': 'нет',
                                  'job': 'нет',
                                  'working': False,
                                  'disease': False,
                                  'username': username,
                                  'last_time': str(datetime.now(tz=tz)).split('.')[0]})
    else:
        if username != user['username']:
            db_data.users.update_one({'user_id': user_id}, {'$set': {'username': username,
                                                                     'last_time': str(datetime.now(tz=tz)).split('.')[
                                                                         0]}})
        else:
            db_data.users.update_one({'user_id': user_id},
                                     {'$set': {'last_time': str(datetime.now(tz=tz)).split('.')[0]}})
