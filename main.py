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

import weaviate
import json


weaviate_client = weaviate.Client("http://202.151.177.149:81")  # Replace with your endpoint
some_objects = weaviate_client.data_object.get()
if (json.dumps(some_objects)):
    print(True)
else:
    print(False)

print(json.dumps(some_objects))

from elasticsearch import Elasticsearch
from json import loads

elastic_client = Elasticsearch("http://202.151.177.154:9200")

response = str(elastic_client.info())
print(response)

def getMLRecommendation(text: str) -> dict:
    # md_text = obj['markdown']
    cur_class = "grandmaster"
    near_text = {"concepts": [text]}
    fetched = (weaviate_client.query
                      .get(CLASS_NAME[cur_class], ["code"])
                      .with_near_text(near_text)
                      .with_limit(1)
                      .do()
                      )
    data = fetched['data']['Get'][CLASS_NAME[cur_class]]
    return data[0]

def getElasticQuery(query, type=["base", "processed"]):
    if (type == "processed"):
        result = {
        "query": {
            "match": {
                "processed": {
                    "query": query
                }
            }
        }
    }
    else:
        result = {
        "query": {
            "match": {
                "markdown": {
                    "query": query
                }
            }
        }
    }
    return result 

def getElasticRecommendation(index, queryBody):
    response = elastic_client.search(index=index, body=queryBody)

    if response and response["hits"]["hits"]:
        result = response["hits"]["hits"][0]["_source"]
        return result['code']
    return []


i = 0
for file_name in FILES:
    with open(file_name, 'r') as file:
        data = json.load(file)

        data_rank = file_name[:-21]

        data_length = len(data)
        data_count = 1
        testing_accumulate = []

        for row in data:
            rows_length = len(row['markdown'])
            row_count = 1

            for markdown in row['markdown']:
                
                temp_result = {
                    "original_md": markdown,
                    "original_code": row['code'],
                    "count": f'{data_count}-{row_count}/{rows_length}',
                    "data_rank": data_rank,
                }
                
                # Get ML Recommendation
                recommended_code_ml = getMLRecommendation(markdown)
                temp_result["recommended_code_ml"] = recommended_code_ml['code']
                # temp_result["model"] = "machine-learning"

                # Get Elastic Recommendation
                query_base = getElasticQuery(markdown)
                query_processed = getElasticQuery(markdown, "processed")
                recommended_code_es_base = getElasticRecommendation(data_rank, query_base)
                recommended_code_es_processed = getElasticRecommendation(data_rank, query_processed)
                temp_result['recommended_code_es_base'] = recommended_code_es_base
                temp_result['recommended_code_es_processed'] = recommended_code_es_processed

                # Append to the collection
                testing_accumulate.append(temp_result)

                print(f'Row Count: {row_count}/{rows_length}')
                row_count = row_count + 1

            print(f'Data Count: {data_count}/{data_length}')
            data_count = data_count + 1


            # if (i==3):
            #     i = 0
            #     break
            # i = i + 1
        
        with open(f"{data_rank}_result.json", "w") as file:
            json.dump(testing_accumulate, file)
            print(f"successfully write to: {data_rank}_result.json ")

print("jobs done!")