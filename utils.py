from typing import Any
import json
from bson import json_util


def get_connection_string() -> str:
    with open("credentials.json") as f:
        connection_string: str = json.load(f)["connection_string"]
    return connection_string


def convert_non_serializable_to_bson(obj: dict):
    return [json.loads(json_util.dumps(news_obj)) for news_obj in obj]


def loads_bson_components(obj: Any):
    return json_util.loads(json_util.dumps(obj))
