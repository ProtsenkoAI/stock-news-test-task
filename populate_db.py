"""Creates 'news' collection and fills it with example news
*warning*: removes all prior news"""
from typing import List
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime
from random import randint, sample, choice
from uuid import uuid4
import argparse

from schemas import News
from utils import get_connection_string


def run(nb_generated_news: int = 10, max_nb_symbols: int = 3):
    client = MongoClient(get_connection_string())

    news_db: Database = client.news_db
    news_collection: Collection = news_db.get_collection("news")

    news_collection.delete_many({})  # remove all elements

    news_handcrafted: List[News] = []
    stock_symbols = ["TSLA", "AAPL", "GOOGL", "AMZN", "NFLX"]

    max_nb_symbols = min(len(stock_symbols), max_nb_symbols)
    for _ in range(nb_generated_news):
        symbols_subset = sample(stock_symbols, randint(1, max_nb_symbols))
        news = News(
                {"publishedAt": datetime.now().isoformat(),
                 "text": "All is fine, stock price rises",
                 "source": choice(["bloomberg", "businesswire", "morningstar"]),
                 "symbols": symbols_subset,
                 "labelsColnames": [],
                 "id": str(uuid4()),
                 }
            )
        news_handcrafted.append(news)

    news_collection.insert_many([news.data for news in news_handcrafted])
    print("Populating succeeded. Exit.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random news and push them to DB")
    parser.add_argument("--cnt_news", type=int, default=10, help="Number of news to generate")
    args = parser.parse_args()
    run(args.cnt_news)
