# fetcher.py

import asyncio
import aiohttp
import feedparser
from models import insert_news_item, init_db
from datetime import datetime
import time

FEEDS_FILE = 'feeds.txt'
CONCURRENT_REQUESTS = 100  # Adjust based on your system's capabilities

async def fetch_feed(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                content = await response.text()
                return content
            else:
                print(f"Failed to fetch {url} with status {response.status}")
                return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def process_feed(session, url):
    content = await fetch_feed(session, url)
    if content:
        feed = feedparser.parse(content)
        source = feed.feed.get('title', url)
        for entry in feed.entries:
            title = entry.get('title', 'No Title')
            link = entry.get('link', '')
            description = entry.get('description', '')
            published_parsed = entry.get('published_parsed')
            if published_parsed:
                published = datetime(*published_parsed[:6])
            else:
                published = datetime.utcnow()
            await insert_news_item(title, link, description, published, source)

async def fetch_all_feeds():
    await init_db()
    with open(FEEDS_FILE, 'r') as f:
        feeds = [line.strip() for line in f if line.strip()]

    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [process_feed(session, url) for url in feeds]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(fetch_all_feeds())
    end_time = time.time()
    print(f"Fetched and processed all feeds in {end_time - start_time:.2f} seconds.")
