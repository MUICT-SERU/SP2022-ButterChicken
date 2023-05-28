import logging
logging.basicConfig(filename='error.log', level=logging.ERROR)
from datetime import datetime
import json
from json import loads
import weaviate
from elasticsearch import Elasticsearch

FILES = [
    "grandmaster_nl_pl_only_plot.json",
    "master_nl_pl_only_plot.json",
    "expert_nl_pl_only_plot.json",
]

CLASS_NAME = {
    "grandmaster": "GrandMasterCode",
    "master": "MasterCode",
    "expert": "ExpertCode",
}




weaviate_client = weaviate.Client("http://202.151.177.149:81")  # Replace with your endpoint
some_objects = weaviate_client.data_object.get()
if (json.dumps(some_objects)):
    print(True)
else:
    print(False)

print(json.dumps(some_objects))


elastic_client = Elasticsearch("http://202.151.177.154:9200")

response = str(elastic_client.info())
# print(response)