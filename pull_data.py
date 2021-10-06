from typing import List
import csv
import json
import warnings
import argparse
from pymongo import MongoClient
from pymongo.collection import Collection

from schemas import news_field_names
from utils import get_connection_string


def pull_news(stock_symbols_csv_path: str, fields: List[str], save_pth: str):
    stock_symbols = _load_onerow_csv(stock_symbols_csv_path)
    if not stock_symbols:
        warnings.warn("Stock symbols is empty, it will result in empty result")
    if not fields:
        warnings.warn("Fields is empty, it will result in empty result")

    client = MongoClient(get_connection_string())
    news_collection: Collection = client.news_db.get_collection("news")

    query = {"symbols": {"$in": stock_symbols}}
    queried_fields = {field: 1 for field in fields}
    queried_fields["id"] = 1  # query it no matter what user says 'cause need it to then write labeled data back
    queried_fields["_id"] = 0  # don't use mongo's _id
    news = list(news_collection.find(query, queried_fields))

    while True:
        try:
            with open(save_pth, "w") as f:
                json.dump(news, f)
            break
        except FileNotFoundError:
            print(f"Can't create file {save_pth}, probably parent directory doesn't exist."
                  f"Save data to another path? (y/[n])")
            try_again = input() == "y"
            if not try_again:
                exit()

    print(f"Successfully wrote news data to {save_pth}")


def _load_onerow_csv(pth: str) -> List:
    """Expects csv with one row, without header"""
    with open(pth) as f:
        csv_reader = csv.DictReader(f, fieldnames=["symbol"])
        symbols = [row["symbol"] for row in csv_reader]
    return symbols


if __name__ == "__main__":
    # TODO: need to check whether fields elements are correct
    parser = argparse.ArgumentParser(description="Generate random news and push them to DB")
    parser.add_argument("--symbols_file_pth", help="Path to one-column, no-header .csv file with stock symbols to seek")
    parser.add_argument("--out_pth", help="path to json file where retrieved data will be stored")
    parser.add_argument("--fields", nargs="+", help=f"List of fields to retrieve. Possible values: {news_field_names}")
    args = parser.parse_args()

    pull_news(args.symbols_file_pth, args.fields, args.out_pth)
