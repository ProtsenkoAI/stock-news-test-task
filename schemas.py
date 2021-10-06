from typing import Dict, Any

from exceptions import WrongFormat

news_basic_field_names = ["id", "publishedAt", "text", "source", "symbols", "labelsColnames"]
news_field_names = news_basic_field_names


class News:
    # pymongo scheme support is poor, so decided to design own schema class
    """Represents news data. Responsible for checking data fields"""
    def __init__(self, news_dict: Dict[str, Any]):
        """
        :param news_dict: dict with following keys: [id, publishedAt, text,
            source, symbols, labelsColnames], and any other colnames listed in labelsColnames.
            Any other set of keys will cause WrongFormat exception.
        """
        if "labelsColnames" not in news_dict:
            raise WrongFormat("news_dict doesn't contain 'labelsColnames' key")
        labels = news_dict["labelsColnames"]
        typed_labels = {col_name: object for col_name in labels}
        self.typed_columns = {
                              "id": str,
                              "publishedAt": str,
                              "text": str,
                              "source": str,
                              "symbols": list,
                              "labelsColnames": list
                              }
        self.dict = {}
        for colname, col_type in {**typed_labels, **self.typed_columns}.items():
            val = news_dict.pop(colname)
            if not isinstance(val, col_type):
                raise WrongFormat(f"{colname} was supposed to have {col_type} type, "
                                  f"but has {type(val)} type")
            self.dict[colname] = val

        if news_dict:
            redundant_colnames = list(news_dict.keys())
            raise WrongFormat(f"Passed columns not listed in default News"
                              f"columns and 'labelsColnames' field: {redundant_colnames}")

    @property
    def data(self) -> dict:
        return self.dict
