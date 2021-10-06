from pymongo import MongoClient
import utils

client = MongoClient(utils.get_connection_string())
# TODO: process pymongo.errors.ConnectionFailure
