from databaseConnections import db_news
from model.models import News
from pymongo import errors


def find_latest_news():
    try:
        news = db_news.find({})
        return news
    except Exception as e:
        print(e.__str__())
        return e

