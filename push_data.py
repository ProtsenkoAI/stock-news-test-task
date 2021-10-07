from typing import List, Dict, Any
import argparse
import json
from pymongo import MongoClient
from pymongo.collection import Collection

import utils
from schema_check import check_news_format
from exceptions import WrongFormat
import constants


def push_data(data_pth: str):
    """
    Pushes labeled data to DB.
    :param data_pth: path to json file with news samples. Every sample should contain _id column, every label column
        added must be listed in labelsColnames field, otherwise WrongFormat will be raised
    """
    with open(data_pth) as f:
        news_data: List[dict] = json.load(f)
    news_data = utils.loads_bson_components(news_data)

    client = MongoClient(utils.get_connection_string())
    news_collection: Collection = client.news_db.get_collection("news")

    for news_sample_data in news_data:
        if "_id" not in news_sample_data:
            raise ValueError("Provided data without id column, can't identify object")
        add_labels_to_news_document(news_sample_data, news_collection)

    print("Successfully wrote labeled data")
    client.close()


def add_labels_to_news_document(labeled: Dict[str, Any], collection):
    """Math labeled data with collection's document, update document and push updated one to DB"""
    if "_id" not in labeled:
        raise WrongFormat("labeled doesn't have _id field, can't match with db")

    db_data_state = collection.find_one({"_id": labeled["_id"]}, {"_id": 0})
    db_data_state.update(labeled)
    consistent_data = db_data_state

    check_news_format(consistent_data, has_id=True)
    collection.find_one_and_replace({"_id": consistent_data["_id"]}, consistent_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get labeled data, match them with db documents and update db")
    parser.add_argument("--data_pth", default=constants.labeled_data_pth, help="Path to json file with data")
    args = parser.parse_args()
    push_data(args.data_pth)
