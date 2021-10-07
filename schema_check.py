from typing import Dict, Any

from exceptions import WrongFormat

news_basic_field_names = ["publishedAt", "text", "source", "symbols", "labelsColnames"]
news_field_names = news_basic_field_names


def check_news_format(news_dict: Dict[str, Any], has_id: bool, must_have_all_required_cols=True):
    # pymongo's support of validator's is poor, and need custom logic for labelsColnames field, so decided to validate
    #   data here
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
    if must_have_all_required_cols:
        required_fields = [*labels, *news_field_names]
    else:
        required_fields = ["labelsColnames"]

    if has_id:
        required_fields.append("_id")

    for colname in required_fields:
        try:
            colnames.remove(colname)
        except ValueError:
            raise WrongFormat(f"key {colname} not found in news_dict, but must exist because it's in "
                              f"labelsColnames list: {labels} or in news_field_names: {news_field_names}."
                              f"Wrong data: {news_dict}")

    if colnames and must_have_all_required_cols:
        raise WrongFormat(f"Passed columns not listed in default News"
                          f"columns and 'labelsColnames' field: {colnames}")
