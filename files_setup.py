"""Script to create required files to speed-up progress"""
import os
import json

import constants


def create_data_dir(data_dir):
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir, exist_ok=False)

    create_stock_symbols_file(data_dir)


def create_credentials_file():
    pth = constants.credentials_pth
    if os.path.isfile(pth):
        print("Credentials file already exists")
    else:
        print("Enter connection string for pymongo")
        connection_string = input()
        data = {
            "connection_string": connection_string
        }
        with open(pth, "w") as f:
            json.dump(data, f)
        print("Successfully created credentials file")


def create_stock_symbols_file(data_dir_pth):
    pth = constants.symbols_file_pth

    if os.path.isfile(pth):
        print("Symbols file already exists")
    else:
        print("Enter stock symbols, delimited by ','. Example: 'GOOGL,AMZN,NFLX'")
        symbols = input().split(",")
        with open(pth, "w") as f:
            for symbol in symbols:
                f.write(symbol + "\n")
        print("Successfully created stock symbols file")


if __name__ == "__main__":
    create_data_dir(constants.DATA_DIR)
    create_credentials_file()
