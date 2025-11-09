#!/usr/bin/env python3
"""
Run multiple database queries concurrently using asyncio.gather and aiosqlite.
"""

import asyncio
import aiosqlite


DB_NAME = "users.db" 


async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users;") as cursor:
            rows = await cursor.fetchall()
            print("All Users:", rows)
            return rows


async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40;") as cursor:
            rows = await cursor.fetchall()
            print("Users older than 40:", rows)
            return rows


async def fetch_concurrently():
   
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )

    all_users, older_users = results
    print("\n=== Concurrent Fetch Completed ===")
    print("Total users:", len(all_users))
    print("Older users:", len(older_users))


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
