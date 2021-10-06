from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection

from utils import get_connection_string


def pull_resources(stock_symbols: List[str], fields: List[str], save_pth: str):
    client = MongoClient(get_connection_string())
    news_collection: Collection = client.news_db.get_collection("news")

    query = {"symbols": {"$in": stock_symbols}}
    queried_fields = {field: 1 for field in fields}
    queried_fields["id"] = 1
    news = news_collection.find(query, queried_fields)
    while True:
        print(news.next())


if __name__ == "__main__":
    pull_resources(["GOOGL", "SOME_WRONG_TICKET"], ["text", "source", "symbols"], "./data/found_resources.json")
