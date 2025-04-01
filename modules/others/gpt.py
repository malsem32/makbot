
from aiogram import types, Router, F
from create_bot import bot
from g4f.client import Client
from g4f.Provider import Bing

router = Router()

@router.message(F.text, lambda message: message.text.split(' ')[0].lower() == 'бот' or message.text.split(' ')[0].lower() == 'бот,')
async def mes(message: types.Message):
    msg = await message.reply('Ищу ответ на ваш вопрос...')
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text.lower().replace('бот ', '')}],
            provider=Bing
        )
        await bot.edit_message_text(response.choices[0].message.content, message.chat.id, msg.message_id)
    except Exception as e:
        print(e)
        await bot.edit_message_text('Что то не так', message.chat.id, msg.message_id)




