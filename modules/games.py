from aiogram import Router, F, types
from create_bot import bot
import asyncio
from database import db_data, cfg_games
from database import check_user
from filters.games import IsSlot, IsDice, IsDarts, IsBowling, IsFootbal, IsBasketball
router = Router()

# Выигрыш
async def win(message, rate_money, amount_money, koff, user_id):
    win_money = int(rate_money * koff)
    end_amount_money = win_money + int(amount_money)
    db_data.users.update_one({'user_id': user_id}, {'$set': {'cash': int(end_amount_money)}})
    await asyncio.sleep(4)
    await message.reply('Ваш выигрыш ===> +' + str(
        f'{await num_triadi(win_money)} $'.replace(',', ' ')), parse_mode='HTML')


# Проигрыш
async def lose(message, amount_money, rate_money, user_id):
    end_amount_money = int(amount_money) - rate_money
    db_data.users.update_one({'user_id': user_id}, {'$set': {'cash': int(end_amount_money)}})
    await asyncio.sleep(4)
    await message.reply('Ваш проигрыш ===> -' + str(
        f'{await num_triadi(rate_money)} $'.replace(',', ' ')), parse_mode='HTML')


# Выигрыш слот
async def win_slot(message, rate_money, amount_money, koff, user_id):
    win_money = int(rate_money * koff)
    end_amount_money = win_money + int(amount_money)
    db_data.users.update_one({'user_id': user_id}, {'$set': {'cash': int(end_amount_money)}})
    await asyncio.sleep(2)
    await message.reply('Ваш выигрыш ===> +' + str(
        f'{await num_triadi(win_money)} $'.replace(',', ' ')), parse_mode='HTML')


# Проигрыш слот
async def lose_slot(message, amount_money, rate_money, user_id):
    end_amount_money = int(amount_money) - rate_money
    db_data.users.update_one({'user_id': user_id}, {'$set': {'cash': int(end_amount_money)}})
    await asyncio.sleep(2)
    await message.reply('Ваш проигрыш ===> -' + str(
        f'{await num_triadi(rate_money)} $'.replace(',', ' ')), parse_mode='HTML')


# Футбол
@router.message(F.text,IsFootbal())
async def get_game_data(message: types.Message):
    user_id = message.from_user.id
    await check_user(message.from_user.id, message.from_user.username)

    text = message.text.capitalize().split()
    value = text[1].split('к')
    money_num = value.pop(0)  # Количество денег (цифры перд К)
    amount_k = len(value)  # Количество К (1к == 1000)
    rate_money = int(money_num) * 1000 ** amount_k  # Ставка
    user_info = db_data.users.find_one({'user_id': user_id})
    amount_money = user_info['cash']
    if rate_money <= amount_money:
        amount_score = await bot.send_dice(message.chat.id, emoji='⚽')
        game_cfg = cfg_games.games.find_one({'name': 'футбол'})
        if amount_score.dice.value == 5:
            await win(message, rate_money, amount_money, game_cfg['first'], user_id)
        elif amount_score.dice.value == 4:
            await win(message, rate_money, amount_money, game_cfg['second'], user_id)
        elif amount_score.dice.value == 3:
            await win(message, rate_money, amount_money, game_cfg['third'], user_id)
        else:
            await lose(message, amount_money, rate_money, user_id)
    else:
        enough_money = rate_money - int(amount_money)
        await message.reply('Вам не хватает: ' + f'{await num_triadi(enough_money)} $\n' + 'Ваш баланс: ' + f'{await num_triadi(amount_money)} $',
                               parse_mode='HTML')

# Баскетбол
@router.message(F.text,IsBasketball())
async def get_game_data(message: types.Message):
    user_id = message.from_user.id
    await check_user(message.from_user.id, message.from_user.username)

    text = message.text.capitalize().split()
    value = text[1].split('к')
    money_num = value.pop(0)  # Количество денег (цифры перд К)
    amount_k = len(value)  # Количество К (1к == 1000)
    rate_money = int(money_num) * 1000 ** amount_k  # Ставка
    user_info = db_data.users.find_one({'user_id': user_id})
    amount_money = user_info['cash']
    if rate_money <= amount_money:
        game_cfg = cfg_games.games.find_one({'name': 'баскетбол'})
        amount_score = await bot.send_dice(message.chat.id, emoji='🏀')
        if amount_score.dice.value == 5:
            await win(message, rate_money, amount_money, game_cfg['first'], user_id)
        elif amount_score.dice.value == 4:
            await win(message, rate_money, amount_money, game_cfg['second'], user_id)
        else:
            await lose(message, amount_money, rate_money, user_id)
    else:
        enough_money = rate_money - int(amount_money)
        await message.reply(
            'Вам не хватает: ' + f'{await num_triadi(enough_money)} $\n' + 'Ваш баланс: ' + f'{await num_triadi(amount_money)} $',
            parse_mode='HTML')

# Кости
@router.message(F.text,IsDice())
async def dice(message: types.Message):
    user_id = message.from_user.id
    await check_user(message.from_user.id, message.from_user.username)

    text = message.text.capitalize().split()
    value = text[1].split('к')
    money_num = value.pop(0)  # Количество денег (цифры перд К)
    amount_k = len(value)  # Количество К (1к == 1000)
    rate_money = int(money_num) * 1000 ** amount_k  # Ставка
    amount_point = text[2]  # Количество точек
    user_info = db_data.users.find_one({'user_id': user_id})
    amount_money = user_info['cash']
    if rate_money <= int(amount_money):
        amount_score = await bot.send_dice(message.chat.id, emoji='🎲')
        game_cfg = cfg_games.games.find_one({'name': 'кости'})
        if int(amount_point) == int(amount_score.dice.value):
            await win(message, rate_money, amount_money, game_cfg['first'], user_id)
        elif abs(int(amount_point) - amount_score.dice.value) == 1:
            await win(message, rate_money, amount_money, game_cfg['second'], user_id)
        else:
            await lose(message, amount_money, rate_money, user_id)
    else:
        enough_money = rate_money - int(amount_money)
        await message.reply(
            'Вам не хватает: ' + f'{await num_triadi(enough_money)} $\n' + 'Ваш баланс: ' + f'{await num_triadi(amount_money)} $',
            parse_mode='HTML')

# Дартс
@router.message(F.text,IsDarts())
async def darts(message: types.Message):
    user_id = message.from_user.id
    await check_user(message.from_user.id, message.from_user.username)

    text = message.text.capitalize().split()
    value = text[1].split('к')
    money_num = value.pop(0)  # Количество денег (цифры перд К)
    amount_k = len(value)  # Количество К (1к == 1000)
    rate_money = int(money_num) * 1000 ** amount_k  # Ставка
    user_info = db_data.users.find_one({'user_id': user_id})
    amount_money = user_info['cash']
    if rate_money <= amount_money:
        amount_score = await bot.send_dice(message.chat.id, emoji='🎯')
        game_cfg = cfg_games.games.find_one({'name': 'дартс'})
        if amount_score.dice.value == 6:
            await win(message, rate_money, amount_money, game_cfg['first'], user_id)
        elif amount_score.dice.value == 5:
            await win(message, rate_money, amount_money, game_cfg['second'], user_id)
        else:
            await lose(message, amount_money, rate_money, user_id)
    else:
        enough_money = rate_money - int(amount_money)
        await message.reply(
            'Вам не хватает: ' + f'{await num_triadi(enough_money)} $\n' + 'Ваш баланс: ' + f'{await num_triadi(amount_money)} $',
            parse_mode='HTML')

# Боулинг
@router.message(F.text,IsBowling())
async def bowling(message: types.Message):
    user_id = message.from_user.id
    await check_user(message.from_user.id, message.from_user.username)

    text = message.text.capitalize().split()
    value = text[1].split('к')
    money_num = value.pop(0)  # Количество денег (цифры перд К)
    amount_k = len(value)  # Количество К (1к == 1000)
    rate_money = int(money_num) * 1000 ** amount_k  # Ставка
    user_info = db_data.users.find_one({'user_id': user_id})
    amount_money = user_info['cash']
    if rate_money <= amount_money:
        amount_score = await bot.send_dice(message.chat.id, emoji='🎳')
        game_cfg = cfg_games.games.find_one({'name': 'боулинг'})
        if amount_score.dice.value == 6:
            await win(message, rate_money, amount_money, game_cfg['first'], user_id)
        elif amount_score.dice.value == 5:
            await win(message, rate_money, amount_money, game_cfg['second'], user_id)
        else:
            await lose(message, amount_money, rate_money, user_id)
    else:
        enough_money = rate_money - int(amount_money)
        await message.reply(
            'Вам не хватает: ' + f'{await num_triadi(enough_money)} $\n' + 'Ваш баланс: ' + f'{await num_triadi(amount_money)} $',
            parse_mode='HTML')

# Слот
@router.message(F.text,IsSlot())
async def slot(message: types.Message):
    user_id = message.from_user.id
    await check_user(message.from_user.id, message.from_user.username)

    text = message.text.capitalize().split()
    value = text[1].split('к')
    money_num = value.pop(0)  # Количество денег (цифры перд К)
    amount_k = len(value)  # Количество К (1к == 1000)
    rate_money = int(money_num) * 1000 ** amount_k  # Ставка
    user_info = db_data.users.find_one({'user_id': user_id})
    amount_money = user_info['cash']
    if rate_money <= amount_money:
        amount_score = await bot.send_dice(message.chat.id, emoji='🎰')
        game_cfg = cfg_games.games.find_one({'name': 'слот'})
        if amount_score.dice.value == 64:
            await win_slot(message, rate_money, amount_money, game_cfg['first'], user_id)
        elif amount_score.dice.value in (1, 22, 43):
            await win_slot(message, rate_money, amount_money, game_cfg['second'], user_id)
        elif amount_score.dice.value in (16, 32, 48):
            await win_slot(message, rate_money, amount_money, game_cfg['third'], user_id)
        else:
            await lose_slot(message, amount_money, rate_money, user_id)
    else:
        enough_money = rate_money - amount_money
        await message.reply(
            'Вам не хватает: ' + f'{await num_triadi(enough_money)} $\n' + 'Ваш баланс: ' + f'{await num_triadi(amount_money)} $',
            parse_mode='HTML')


# разбитие на триады
async def num_triadi(num):
    return "{:,}".format(num).replace(",", " ")

