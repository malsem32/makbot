from aiogram import types
from aiogram.filters import BaseFilter
# Фильтр футбол
class IsFootbal(BaseFilter):
    async def __call__(self, message: types.Message):
        text = message.text.capitalize().split()
        try:
            value = text[1].split('к')
            money_num = value.pop(0)  # Количество денег (цифры перд К)
            amount_k = len(value)  # Количество К (1к == 1000)
            return text[0] == 'Гол' and len(text) == 2 and int(money_num) >= 1 and amount_k >= 0
        except IndexError:
            return False
        except ValueError:
            return False


# Фильтр баксетбол
class IsBasketball(BaseFilter):
    async def __call__(self, message: types.Message):
        text = message.text.capitalize().split()
        try:
            value = text[1].split('к')
            money_num = value.pop(0)  # Количество денег (цифры перд К)
            amount_k = len(value)  # Количество К (1к == 1000)
            return (text[0] == 'Баскетбол' or text[0] == 'Баск') and len(text) == 2 and int(
                money_num) >= 1 and amount_k >= 0
        except IndexError:
            return False
        except ValueError:
            return False


# Фильтр кости
class IsDice(BaseFilter):
    async def __call__(self, message: types.Message):
        text = message.text.capitalize().split()
        try:
            value = text[1].split('к')
            amount_point = text[2]
            money_num = value.pop(0)  # Количество денег (цифры перд К)
            amount_k = len(value)  # Количество К (1к == 1000)
            return text[0] == 'Кости' and len(text) == 3 and int(
                money_num) >= 1 and amount_k >= 0 and (1 <= int(amount_point) <= 6)
        except IndexError:
            return False
        except ValueError:
            return False


# Фильтр дартс
class IsDarts(BaseFilter):
    async def __call__(self, message: types.Message):
        text = message.text.capitalize().split()
        try:
            value = text[1].split('к')
            money_num = value.pop(0)  # Количество денег (цифры перд К)
            amount_k = len(value)  # Количество К (1к == 1000)
            return text[0] == 'Дартс' and len(text) == 2 and int(
                money_num) >= 1 and amount_k >= 0
        except IndexError:
            return False
        except ValueError:
            return False


# Фильтр боулинг
class IsBowling(BaseFilter):
    async def __call__(self, message: types.Message):
        text = message.text.capitalize().split()
        try:
            value = text[1].split('к')
            money_num = value.pop(0)  # Количество денег (цифры перд К)
            amount_k = len(value)  # Количество К (1к == 1000)
            return text[0] == 'Боулинг' and len(text) == 2 and int(
                money_num) >= 1 and amount_k >= 0
        except IndexError:
            return False
        except ValueError:
            return False


# Фильтр слот
class IsSlot(BaseFilter):
    async def __call__(self, message: types.Message):
        text = message.text.capitalize().split()
        try:
            value = text[1].split('к')
            money_num = value.pop(0)  # Количество денег (цифры перд К)
            amount_k = len(value)  # Количество К (1к == 1000)
            return text[0] == 'Слот' and len(text) == 2 and int(
                money_num) >= 1 and amount_k >= 0
        except IndexError:
            return False
        except ValueError:
            return False