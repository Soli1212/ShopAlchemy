from asyncio import run

from connection import async_session, init_db
from models import *
#


async def main():
    await init_db()


if __name__ == "__main__":
    run(main=main())