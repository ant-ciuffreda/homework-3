import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()
client = Elasticsearch(
    os.getenv("ES_URL"),
    basic_auth=(os.getenv("ES_USER"), os.getenv("ES_PASSWORD")),
)
print(client.info())
