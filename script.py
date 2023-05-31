import logging
logging.basicConfig(filename='error.log', level=logging.ERROR)
from datetime import datetime
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

import json
from json import loads
import weaviate
from elasticsearch import Elasticsearch


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

def getMLRecommendation(text: str, target_class: str) -> dict:
    # md_text = obj['markdown']
    # cur_class = "grandmaster"
    near_text = {"concepts": [text]}
    fetched = (weaviate_client.query
                      .get(CLASS_NAME[target_class], ["code"])
                      .with_near_text(near_text)
                      .with_limit(1)
                      .do()
                      )
    data = fetched['data']['Get'][CLASS_NAME[target_class]]
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
        return result
    return []

for file_name in FILES:
    with open(f'data/{file_name}', 'r') as file:
        data = json.load(file)
        data_rank = file_name[:-21]

        data_length = len(data)
        testing_accumulate = []
        count = 0
        for row in data:

            markdown = "".join(row['markdown'])
            
            print(f"markdown length: {len(markdown)}")
            try:

                temp_result = {
                    "running_count_label": count,
                    "data_rank": data_rank,
                    "original": {
                        "markdown": markdown,
                        "code": row['code'],
                        "processed_markdown": row['processed'],
                    },
                    # Template for insert
                    "mlRecommendation": {
                        "code": ""
                    },
                    "bm25Recommendation": {
                        "markdown": "",
                        "processed_markdown": "",
                        "code": "",
                    },
                    "bm25ProcessedRecommendation": {
                        "markdown": "",
                        "processed_markdown": "",
                        "code": ""
                    }
                }

                # Get ML Recommendation
                recommended_code_ml = getMLRecommendation(markdown, data_rank)
                temp_result["mlRecommendation"]["code"] = recommended_code_ml['code']
            
                # Get Elastic Recommendation
                query_base = getElasticQuery(markdown)
                query_processed = getElasticQuery(markdown, "processed")

                recommended_code_es_base = getElasticRecommendation(data_rank, query_base)
                recommended_code_es_processed = getElasticRecommendation(data_rank, query_processed)

                temp_result["bm25Recommendation"]["markdown"] = recommended_code_es_base['markdown']
                temp_result["bm25Recommendation"]["processed_markdown"] = recommended_code_es_base['processed']
                temp_result["bm25Recommendation"]["code"] = recommended_code_es_base['code']

                temp_result["bm25ProcessedRecommendation"]["markdown"] = recommended_code_es_base['markdown']
                temp_result["bm25ProcessedRecommendation"]["processed_markdown"] = recommended_code_es_base['processed']
                temp_result["bm25ProcessedRecommendation"]["code"] = recommended_code_es_base['code']

                # Append to the collection
                testing_accumulate.append(temp_result)

                print(f'Count: {count}/{data_length}')
                
            except Exception as e:
                print(f'[{datetime.now().strftime("%d/%m/%y %H:%M:%S")}] Skipping item #{count} due to an error.')
                logging.error(f"Error occurred for item: {markdown}\nError message: {str(e)}\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
                continue
            count =  count + 1
        
        with open(f"recommendation-result/{data_rank}_result.json", "w") as file:
            json.dump(testing_accumulate, file)
            print(f"successfully write to: {data_rank}_result.json ")

output = {}
metadata = {}
FILE_NAMES = [
    "grandmaster_result.json",
    "master_result.json",
    "expert_result.json",
]
for name in FILE_NAMES:
    path = f"recommendation-result/{name}"
    data_rank = name[:-12]

    with open(path, 'r') as file:
        original_file_path = open(f'data/{data_rank}_nl_pl_only_plot.json')
        original_data = json.load(original_file_path)
        
        data = json.load(file)
        print(f"rank {data_rank}: {len(data)} items || original : {len(original_data)} items")

        comparison_collection = {
            "ml": 0,
            "es": 0,
            "es-processed": 0,
        }
        incorrect_summarize = {
            # "ml": 0,
            "es": 0,
            # "es-processed": 0,
        }

        incorrect_pairs = []
        incorrect = {

        }
        i = 0
        count_empty = 0
        for item in data:
            if (not item['original']['markdown']):
                count_empty = count_empty + 1
                continue

            ml_recommendation = item['mlRecommendation']
            bm25_base_recommendation = item['bm25Recommendation']
            bm25_processed_recommendation = item['bm25ProcessedRecommendation']
            
            original = item['original']

            # ML
            if (original['code']==ml_recommendation['code']):
                comparison_collection["ml"] = comparison_collection["ml"] + 1
            
            # BM25 processeds
            if (original['code']==bm25_processed_recommendation['code']):
                comparison_collection["es-processed"] = comparison_collection["es-processed"] + 1

            # BM25 base
            if (original['code']==bm25_base_recommendation['code']):
                comparison_collection["es"] = comparison_collection["es"] + 1
            else:                
                incorrect_summarize["es"] = incorrect_summarize["es"] + 1
                incorrect_pairs.append({
                    "original_markdown": original['markdown'],
                    "original_code": original['code'],
                    "bm25_markdown": bm25_base_recommendation['markdown'],
                    "bm25_code": bm25_base_recommendation['code'],
                    "ml_code": ml_recommendation['code']
                })
            
        
        print(f"Skipped {count_empty} empty Markdown items in rank {data_rank}")
        
        output[data_rank] = {
            "correct_pairs_summarize": comparison_collection,
            "incorrect_summarize": {
                "es": len(data)-count_empty-comparison_collection["es"]
            },
            "incorrect_pairs_items": incorrect_pairs,
        }

        metadata[data_rank] = {
            "total_items": len(data),
            "total_skipped_empty_markdown": count_empty,
            "total_es_correct_pairs_": comparison_collection["es"],
            "total_es_incorrect_pairs_": incorrect_summarize["es"]
        }
        
with open(f"comparison_result.json", "w") as file:
    output = json.dump(output, file)
    print(f'successfully write to /result/comparison_result.json')
print("Done!!")

print(f"""
Summarize:

Rank Grandmaster
- Total items: {metadata['grandmaster']["total_items"]}
- Total skipped empty Markdown: {metadata['grandmaster']["total_skipped_empty_markdown"]}
# Below is only for Elasticsearch base approach #
- Total correct original-recommended pairs: {metadata['grandmaster']["total_es_correct_pairs_"]}
- Total incorrect original-recommended pairs: {metadata['grandmaster']["total_es_incorrect_pairs_"]}

Rank Master
- Total items: {metadata['master']["total_items"]}
- Total skipped empty Markdown: {metadata['master']["total_skipped_empty_markdown"]}
# Below is only for Elasticsearch base approach #
- Total correct original-recommended pairs: {metadata['master']["total_es_correct_pairs_"]}
- Total incorrect original-recommended pairs: {metadata['master']["total_es_incorrect_pairs_"]}

Rank Expert
- Total items: {metadata['expert']["total_items"]}
- Total skipped empty Markdown: {metadata['expert']["total_skipped_empty_markdown"]}
# Below is only for Elasticsearch base approach #
- Total correct original-recommended pairs: {metadata['expert']["total_es_correct_pairs_"]}
- Total incorrect original-recommended pairs: {metadata['expert']["total_es_incorrect_pairs_"]}
""")

import random 
RANKS = ['grandmaster', 'master', 'expert']
MAX_SAMPLE = 30

with open("comparison_result.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for rank in RANKS:
        incorrect_pairs = data[rank]['incorrect_pairs_items']
        with open(f'./analysis-result/{rank}_analysis.txt', 'w', encoding="utf-8") as file:
            random_range = list(range(0, len(incorrect_pairs)))
            random.shuffle(random_range)
            i = 0
            while i<MAX_SAMPLE:
                if (i>=MAX_SAMPLE):
                    break
                print(f"i = {i}")

                file.write(f"ITEM #{i+1}\n\n")
                file.write(f"ORIGINAL MARKDOWN:\n{'-'*30}\n")
                file.write(str(incorrect_pairs[i]['original_markdown']))
                file.write(f"\n{'='*30}\n")

                file.write(f"RECOMMENDED MARKDOWN:\n{'-'*30}\n")
                file.write(str(incorrect_pairs[i]['bm25_markdown'][0]))
                file.write(f"\n{'='*30}\n")
                
                file.write(f"ORIGINAL CODE:\n{'-'*30}\n")
                file.write(str(incorrect_pairs[i]['original_code']))
                file.write(f"\n{'='*30}\n")
                
                file.write(f"RECOMMENDED CODE:\n{'-'*30}\n")
                file.write(str(incorrect_pairs[i]['bm25_code']))
                file.write(f"\n{'='*30}\n")

                file.write(f"RECOMMENDED MACHINE LEARNING CODE:\n{'-'*30}\n")
                file.write(str(incorrect_pairs[i]['ml_code']))
                file.write("\n" + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"*2 + "\n")

                i = i+1

print('Everything finish') 