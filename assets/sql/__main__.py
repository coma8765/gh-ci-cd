import asyncio
import os

import asyncpg


async def main():
    print("[ + ] Startup table creator.")
    conn: asyncpg.Connection = await asyncpg.connect(
        f"postgresql://"
        f"{os.getenv('POSTGRES_USER', None) or 'postgres'}:"
        f"{os.getenv('POSTGRES_PASSWORD', None) or 'password'}@"
        f"{os.getenv('POSTGRES_HOST', None) or 'localhost'}:"
        f"{os.getenv('POSTGRES_PORT', None) or 5432}/"
        f"{os.getenv('POSTGRES_DATABASE', None) or 'postgres'}",
    )
    async with conn.transaction() as tr:
        for file in reversed(list(filter(
                lambda x: x.startswith("create_"),
                os.listdir(os.path.dirname(__file__))
        ))):
            with open(f"{os.path.dirname(__file__)}/{file}") as f:
                await conn.execute(f.read())
                print(f"[ + ] Added tables from file \"{file}\".")

    await conn.close()
    print(f"[ + ] Shutdown tables creator.")

asyncio.run(main())
