from typing import List
import csv
import json
import warnings
import argparse
from pymongo import MongoClient
from pymongo.collection import Collection

import utils
from schema_check import check_news_format, news_field_names
from utils import get_connection_string
import constants


def pull_news(stock_symbols_csv_path: str, fields: List[str], save_pth: str):
    stock_symbols = _load_onerow_csv(stock_symbols_csv_path)
    check_input(stock_symbols, fields)

    client = MongoClient(get_connection_string())
    news_collection: Collection = client.news_db.get_collection("news")

    query = {"symbols": {"$in": stock_symbols}}
    # need to add this field, otherwise errors it situation if do labeling > 1 time will occur. For example,
    # at first run add column "target", at second run add column "class". Second run need to push ["target", "class"]
    # in "labelsColnames"
    if "labelsColnames" not in fields:
        fields.append("labelsColnames")
    queried_fields = {field: 1 for field in fields}
    all_news = list(news_collection.find(query, queried_fields))
    # encode from bson _id object to serializable
    all_news = utils.convert_non_serializable_to_bson(all_news)

    for news_obj in all_news:

        check_news_format(news_obj, has_id=True, must_have_all_required_cols=False)

    write_success = write_data(all_news, save_pth)
    if write_success:
        print(f"Successfully wrote news data to {save_pth}")
    else:
        print("Failed to write data.")
    client.close()


def check_input(stock_symbols: List[str], fields: List[str]):
    non_standard_fields = set(news_field_names).difference(fields)
    if non_standard_fields:
        warnings.warn(f"Found unusual fields in your query, that don't match standard data fields: "
                      f"{non_standard_fields}. They will be queried, but it's not guaranteed that they'll be found")

    if not stock_symbols:
        warnings.warn("Stock symbols is empty, it will result in empty result")
    if not fields:
        warnings.warn("Fields is empty, it will result in empty result")


def write_data(all_news: List[dict], save_pth: str) -> bool:
    """Tries to write costly-obtained data to file. If fails to write, tries again with new path provided by user in
    std input, unless user manually cancels operation"""
    while True:
        try:
            with open(save_pth, "w") as f:
                json.dump(all_news, f)
            return True
        except FileNotFoundError:
            print(f"Can't create file {save_pth}, probably parent directory doesn't exist."
                  f"Save data to another path? (y/[n])")
            try_again = input() == "y"
            if not try_again:
                return False


def _load_onerow_csv(pth: str) -> List:
    """Expects csv with one row, without header"""
    with open(pth) as f:
        csv_reader = csv.DictReader(f, fieldnames=["symbol"])
        symbols = [row["symbol"] for row in csv_reader]
    return symbols


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random news and push them to DB")
    parser.add_argument("--symbols_file_pth", default=constants.symbols_file_pth,
                        help="Path to one-column, no-header .csv file with stock symbols to seek")
    parser.add_argument("--out_pth", default=constants.downloaded_data_pth,
                        help="path to json file where retrieved data will be stored")
    parser.add_argument("--fields", default=",".join(news_field_names),
                        nargs="+", help=f"List of fields to retrieve, delimited by ','. "
                                        f"Possible values: {news_field_names}")
    args = parser.parse_args()

    pull_news(args.symbols_file_pth, args.fields.split(","), args.out_pth)
