import requests
from schemas.product import ProductSchema

async def parse(id):
    response = requests.get(
    f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-5818883&spp=30&ab_testing=false&nm={id}')
    item = ProductSchema.model_validate(response.json()['data']['products'][0]).model_dump(by_alias=False)
    return item