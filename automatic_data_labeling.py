"""Script to imitate data labeling for testing purposes"""
from typing import Dict, List, Any
from random import choice
import json
import argparse
import os

import constants

example_label_cols_to_values = json.dumps({"target": [1, 2, 3], "target_std": [0.02, 0.5, 0.04]})


def create_labeled_data(inp_pth: str, out_pth: str, labels_colnames2poss_values: Dict[str, List[Any]]):
    f"""
    Read data, imitate labels, save.
    :param inp_pth: path to .json with input data
    :param out_pth: pth to .json where to save labeled data
    :param labels_colnames2poss_values: mapping from label_colnames to possible values of this column.
    Example: {example_label_cols_to_values}
    """
    with open(inp_pth) as f:
        data = json.load(f)

    for sample in data:
        for colname, poss_values in labels_colnames2poss_values.items():
            sample[colname] = choice(poss_values)
            sample["labelsColnames"].append(colname)

    with open(out_pth, "w") as f:
        json.dump(data, f)
    print("Successfully saved labeled data")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate labeled file from news downloaded from DB"
                                                 "all existing data.")
    parser.add_argument("--inp_pth", default=constants.downloaded_data_pth, help="Path to unlabeled data")
    parser.add_argument("--out_pth", default=constants.labeled_data_pth, help="Path where to save labeled data")
    parser.add_argument("--labels_colnames_to_values", default=example_label_cols_to_values,
                        help="JSON-format string with possible values of label colnames"
                             f'Example: {example_label_cols_to_values}')
    args = parser.parse_args()

    inp_pth = os.path.join(constants.DATA_DIR, "found_resources")
    create_labeled_data(args.inp_pth, args.out_pth, json.loads(args.labels_colnames_to_values))
