#!/usr/bin/env python3
import asyncio
import aiosqlite

database_path = "/home/moment/alx-backend-python/python-decorators-0x01/users.db"

async def async_fetch_users():
    """" Connect to the database and fetch users"""""
    try:
        db = await aiosqlite.connect(database_path)
        cursor = await db.execute('SELECT * FROM users')
        all_users = await cursor.fetchall()
        for user in all_users:
            print(user)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await cursor.close()
        await db.close()
    


async def async_fetch_older_users():
    """" Connect to the database and fetch users"""""
    try:
        db = await aiosqlite.connect(database_path)
        cursor = await db.execute('SELECT * FROM users WHERE age > ?', (40, ))
        users_older = await cursor.fetchall()
        for user_older in users_older:
            print(user_older)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await cursor.close()
        await db.close()
    return users_older


async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()

    )

asyncio.run(fetch_concurrently())
