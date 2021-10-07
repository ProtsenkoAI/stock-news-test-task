from typing import Dict, Any

from exceptions import WrongFormat

# TODO: replace id support with _id
news_basic_field_names = ["publishedAt", "text", "source", "symbols", "labelsColnames"]
news_field_names = news_basic_field_names


class News:
    # pymongo scheme support is poor, so decided to design own schema class
    # TODO: convert to functions
    @staticmethod
    def check_format(news_dict: Dict[str, Any], has_id):
        """
        :param news_dict: dict, has following keys: [publishedAt, text, source, symbols, labelsColnames],
            and any other colnames listed in labelsColnames.
            Any other set of keys will cause WrongFormat exception.
        :param has_id: bool, whether data has mongo's _id field or not.
        """
        if "labelsColnames" not in news_dict:
            raise WrongFormat("news_dict doesn't contain 'labelsColnames' key")

        colnames = list(news_dict.keys())
        labels = news_dict["labelsColnames"]
        required_fields = [*labels, news_field_names]
        if has_id:
            required_fields.append("_id")

        for colname in required_fields:
            try:
                colnames.remove(colname)
            except ValueError:
                raise WrongFormat(f"key {colname} not found in news_dict, but must exist because it's in "
                                  f"labelsColnames list: {labels} or in news_field_names: {news_field_names}")

        if news_dict:
            redundant_colnames = list(news_dict.keys())
            raise WrongFormat(f"Passed columns not listed in default News"
                              f"columns and 'labelsColnames' field: {redundant_colnames}")

    @staticmethod