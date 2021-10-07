import os

credentials_pth = "./credentials.json"
DATA_DIR = "./data"
symbols_file_pth = os.path.join(DATA_DIR, "stock_symbols.csv")
downloaded_data_pth = os.path.join(DATA_DIR, "found_resources.json")
labeled_data_pth = os.path.join(DATA_DIR, "labeled_data.json")
