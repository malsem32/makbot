from aiogram import types, Router, F
from database import db_data, check_user
from create_bot import bot
from datetime import datetime
import random
from aiogram.filters import Command

router = Router()


@router.message(Command('bonus'))
async def bonus(message: types.Message):
    await check_user(message.from_user.id, message.from_user.username)
    members = await bot.get_chat_member(chat_id=-1001879290440, user_id=message.from_user.id)
    now = datetime.now()
    if members.status != 'left':
        bonus_info = db_data.bonus.find_one({'user_id': message.from_user.id})
        if bonus_info is None:

            db_data.bonus.insert_one({
                'user_id': message.from_user.id,
                'date': now.day
            })
            rnd_cash = random.randint(1000, 30000)
            user_info = db_data.users.find_one({'user_id': message.from_user.id})
            db_data.users.update_one({'user_id': message.from_user.id}, {'$set': {'cash': user_info['cash'] + rnd_cash}})
            await message.reply(f'Ваш бонус на сегодняшний день {await num_triadi(rnd_cash)}$', parse_mode='HTML')
        else:
            if now.day == bonus_info['date']:
                await message.reply('Вы уже получали сегодня бонус!', parse_mode='HTML')
            else:
                db_data.bonus.insert_one({
                    'user_id': message.from_user.id,
                    'date': now.day
                })
                rnd_cash = random.randint(1000, 30000)
                user_info = db_data.users.find_one({'user_id': message.from_user.id})
                db_data.users.update_one({'user_id': message.from_user.id},
                                         {'$set': {'cash': user_info['cash'] + rnd_cash}})
                await message.reply(f'Ваш бонус на сегодняшний день {await num_triadi(rnd_cash)}$', parse_mode='HTML')
    else:
        await message.reply(f'Чтобы получить бонус, вы должны состоять в моем канале @makbotinfo', parse_mode='HTML')

@router.message(F.text, lambda message: 'бонус' == message.text.lower())
async def bonus_t(message: types.Message):
    await bonus(message)

# разбитие на триады
async def num_triadi(num):
    return "{:,}".format(num).replace(",", " ")