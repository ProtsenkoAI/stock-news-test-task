"""Creates 'news' collection and fills it with example news
*warning*: removes all prior news"""
from typing import List
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime
from random import randint, sample, choice
import argparse

from schema_check import check_news_format
from utils import get_connection_string


def generate_and_push_samples(nb_generated_news: int = 10, max_nb_symbols: int = 3):
    """
    Creates nb_generated_news news objects using random or default fillings to fields and push them to db
    :param nb_generated_news: number of samples to generate
    :param max_nb_symbols: maximum number of companies' symbols occurring in one news.
    """
    client = MongoClient(get_connection_string())
    news_db: Database = client.news_db
    news_collection: Collection = news_db.get_collection("news")
    news_collection.delete_many({})  # remove all elements

    news_handcrafted: List[dict] = []
    stock_symbols = ["TSLA", "AAPL", "GOOGL", "AMZN", "NFLX"]

    max_nb_symbols = min(len(stock_symbols), max_nb_symbols)
    for _ in range(nb_generated_news):
        symbols_subset = sample(stock_symbols, randint(1, max_nb_symbols))
        news = {"publishedAt": datetime.now().isoformat(),
                "text": "All is fine, stock price rises",
                "source": choice(["bloomberg", "businesswire", "morningstar"]),
                "symbols": symbols_subset,
                "labelsColnames": [],
                }
        check_news_format(news, has_id=False)
        news_handcrafted.append(news)

    news_collection.insert_many(news_handcrafted)
    print("Populating succeeded. Exit.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random news and push them to DB. ATTENTION: it'll remove "
                                                 "all existing data.")
    parser.add_argument("--cnt_news", type=int, default=10, help="Number of news to generate")
    args = parser.parse_args()
    generate_and_push_samples(args.cnt_news)
