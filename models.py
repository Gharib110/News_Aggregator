# models.py

import aiosqlite
import asyncio
from datetime import datetime

DB_NAME = 'news.db'

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE,
                description TEXT,
                published DATETIME,
                source TEXT
            )
        ''')
        await db.commit()

async def insert_news_item(title, link, description, published, source):
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute('''
                INSERT INTO news (title, link, description, published, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, link, description, published, source))
            await db.commit()
        except aiosqlite.IntegrityError:
            # Duplicate entry based on UNIQUE link
            pass

async def fetch_news(skip=0, limit=50):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''
            SELECT title, link, description, published, source
            FROM news
            ORDER BY published DESC
            LIMIT ? OFFSET ?
        ''', (limit, skip))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def get_total_news_count():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT COUNT(*) FROM news')
        count = await cursor.fetchone()
        await cursor.close()
        return count[0]
