from aiogram import Bot, Dispatcher, F
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
from aiohttp import ClientSession

from dotenv import load_dotenv
load_dotenv()

bot = Bot(getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Пожалуйста введите артикул товара: ")

@dp.message(F.text.regexp(r'^\d+$'))
async def product_handler(message: Message) -> None:
    try:
        id_product = message.text
        url = f'http://127.0.0.1:8000/api/v1/product/{id_product}'
        async with ClientSession() as session:
            async with session.get(
                url=url
            ) as response:
                data = await response.json()
                print(data)

                try:
                    quantity_by_sizes = data.pop('quantity_by_sizes')
                    
                    product = f'Артикул товара:  {data["nm_id"]}\n'\
                            f'Стоимость товара:  {data["current_price"]}\n'\
                            f'Количество товара:  {data["sum_quantity"]}\n'
                    
                    await message.answer(product)
                                
                    for size in quantity_by_sizes:
                        quantity_by_wh = size.pop('quantity_by_wh')
                        print(quantity_by_wh)
                        size = f'Доступный размер: {size["size"]}\n'

                        for wh in quantity_by_wh:
                            print(wh)
                            row = f'На складе {wh["wh"]} осталось {wh["quantity"]} товаров\n'
                            size = size + row
                        size = size + '\n'
                        await message.answer(size)
                except (IndexError, KeyError):
                    await message.answer('Не удалось найти товар.')
    except Exception as e:
        await message.answer(f"Возникла ошибка, {e}.")

@dp.message()
async def answer(message: Message) -> None:
    await message.answer(
        f'Бот принимает только артикультые номера. \nОни состоят из цифр.')



if __name__ == "__main__":
    #asyncio.run(main())
    asyncio.run(dp.start_polling(bot))