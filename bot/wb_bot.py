import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()

bot = Bot(getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Пожалуйста, введите артикул товара: ')


@dp.message(F.text.regexp(r'^\d+$'))
async def product_handler(message: Message) -> None:
    try:
        id_product = message.text
        url = f'http://web_fastapi:8000/api/v1/product/{id_product}'
        async with ClientSession() as session:
            async with session.get(
                url=url
            ) as response:
                data = await response.json()
                try:
                    quantity_by_sizes = data.pop('quantity_by_sizes')

                    product = f'Артикул товара:  {data["nm_id"]}\n'\
                              f'Стоимость товара:  {data["current_price"]}\n'\
                              f'Количество товара:  {data["sum_quantity"]}\n'
                    await message.answer(product)

                    for size in quantity_by_sizes:
                        quantity_by_wh = size.pop('quantity_by_wh')
                        size = f'Доступный размер: {size["size"]}\n'

                        for wh in quantity_by_wh:
                            row = f'На складе {wh["wh"]} '\
                                  f'осталось {wh["quantity"]} товаров\n'
                            size = size + row
                        size = size + '\n'
                        await message.answer(size)
                except (IndexError, KeyError):
                    await message.answer('Не удалось найти товар.')
    except Exception as e:
        await message.answer(f'Возникла ошибка: {e}.')


@dp.message()
async def other_handler(message: Message) -> None:
    await message.answer(
        'Бот принимает только артикульные номера.')


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
