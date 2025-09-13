from asyncio import run
from pprint import pprint

from RedisServices.connection import RedisConnection
from RedisServices.services import UserCartService


async def main():
    connection = await RedisConnection.connect()
    c = UserCartService(redis_client=connection)
    await c.add_item("soheil", "variant_1", 2)
    await c.add_item("soheil", "variant_2", 3)
    c.edit_item("soheil", "variant_1", 5)
    r = await c.get_cart("soheil")
    pprint(r, sort_dicts=True)


if __name__ == "__main__":
    run(main=main())
