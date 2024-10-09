# app.py

from flask import Flask, render_template, request
import asyncio
from models import fetch_news, get_total_news_count, init_db
from fetcher import fetch_all_feeds
from apscheduler.schedulers.background import BackgroundScheduler
import logging

app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the database and scheduler
asyncio.run(init_db())

scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: asyncio.run(fetch_all_feeds()), trigger="interval", minutes=1)
scheduler.start()

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    limit = 50
    skip = (page - 1) * limit
    logger.info(f"Fetching news: page={page}, skip={skip}, limit={limit}")
    news = asyncio.run(fetch_news(skip=skip, limit=limit))
    logger.info(f"Number of news items fetched: {len(news)}")
    total = asyncio.run(get_total_news_count())
    logger.info(f"Total news items in database: {total}")
    total_pages = (total + limit - 1) // limit
    return render_template('index.html', news=news, page=page, total_pages=total_pages)

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        pass
