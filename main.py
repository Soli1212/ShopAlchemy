from asyncio import run

from connection import async_session, init_db
from models import *
from repositories.user_address_repository import UserAddressRepository


async def main():
    # await init_db()

    async with async_session() as session:
        async with session.begin():
            repo = UserAddressRepository(session)
            addr = await repo.count_user_addresses(user_id="15a9f02a-6db3-4eb6-9faf-e21ad5fd2ccd")
            print(addr)



if __name__ == "__main__":
    run(main=main())
