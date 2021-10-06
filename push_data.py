from typing import List
import argparse
import json
from pymongo import MongoClient
from pymongo.collection import Collection

from utils import get_connection_string
from schemas import News


def push_data(data_pth: str):
    # TODO: replace News constructor with simple check of consistency
    # TODO: upload data
    with open(data_pth) as f:
        news_data: List[dict] = json.load(f)

    client = MongoClient(get_connection_string())
    news_collection: Collection = client.news_db.get_collection("news")

    for news_sample_data in news_data:
        if "id" not in news_sample_data:
            raise ValueError("Provided data without id column, can't identify object")

        old_full_data = news_collection.find_one({"id": news_sample_data["id"]}, {"_id": 0})

        old_full_data.update(news_sample_data)
        consistent_data = News(old_full_data).data
        print(consistent_data)

        news_collection.find_one_and_replace({"id": consistent_data["id"]}, consistent_data)
    print("Successfully wrote labeled data")


if __name__ == "__main__":
    # TODO: need to check whether fields elements are correct
    parser = argparse.ArgumentParser(description="Generate random news and push them to DB")
    parser.add_argument("--data_pth", help="Path to json file with data")
    args = parser.parse_args()
    push_data(args.data_pth)
