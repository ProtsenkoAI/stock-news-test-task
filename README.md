# Stock news test task

### Install
pre-requirements:
1. python
2. pip
3. pipenv:  ```pip install pipenv```
```
git clone git@github.com:ProtsenkoAI/stock-news-test-task.git
cd stock-news-test-task
pipenv install
pipenv shell
```
## Example flow:
### Prepare files
creates credentials.json and data/.Example:
```
python3 ./files_setup.py
```
### Populate database with data
Fills db with random-generated data for testing purposes. Example:
```
python3 ./populate_db.py --cnt_news 8
```
### Download data specifying stocks & data fields
Example:
```
python3 ./pull_data.py --symbols_file_pth ./data/stock_symbols.csv \
--fields publishedAt text source --out_pth ./data/found_resources.json
```
### Run labeling
For example, can convert sample {"_id": ..., "text": ..., "labelsColumns": []} to:

{"_id": ..., "text": ..., "labelsColumns": ["target", "targetStd"], "target": 2.0, "targetStd": 0.03}

Example:
```
python3 ./automatic_data_labeling.py --inp_pth ./data/found_resources.json \
--out_pth ./data/labeled_data.json --labels_colnames_to_values '{"target": [1, 2, 3]}'
```
### Update labeled data in DB
Example:
```
python3 ./push_data.py --data_pth ./data/labeled_data.json
```