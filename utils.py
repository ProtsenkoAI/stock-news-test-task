import json


def get_connection_string() -> str:
    with open("credentials.json") as f:
        connection_string: str = json.load(f)["connection_string"]
    return connection_string
