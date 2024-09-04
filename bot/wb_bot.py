from aiogram import Bot, Dispatcher, exceptions, F

import asyncio
import logging
import sys
from os import getenv
import requests
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7061498716:AAEgM90X5zncjb_j5pT-0gPo6Wl-qD3e5c8"
bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Пожалуйста введите артикул товара: ")



@dp.message(F.text.regexp(r'(?<![-.])\b[0-9]+\b(?!\.[0-9])'))
#@dp.message()#F.text.regexp(r'(?<![-.])\b[0-9]+\b(?!\.[0-9])'))
async def product_handler(message: Message) -> None:
    try:
        # Send a copy of the received message
        
        id_product = message.text
        url = f'http://127.0.0.1:8000/api/v1/product/{id_product}'
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(
        #         url=url
        #     )

#bot = Bot(..., session=session)
        # id_product = message.text
        # url = f'http://127.0.0.1:8000/api/v1/product/{id_product}'
        response = requests.get(url)
        data = await response.json()
        print(data)
        return message.answer(data)

        #await message.send_copy(chat_id=message.chat.id)
    except Exception as e:
        # But not all the types is supported to be copied so need to handle it
        await message.answer(f"Возникла ошибка, {e}")


# async def main() -> None:
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    #asyncio.run(main())
    asyncio.run(dp.start_polling(bot))