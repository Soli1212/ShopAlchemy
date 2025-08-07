from asyncio import run

from connection import async_session, init_db
from models import *
from repositories.user_repository import UserRepository


async def main():
    # await init_db()

    async with async_session() as session:
        async with session.begin():
            ...


if __name__ == "__main__":
    run(main=main())
