import multiprocessing
from math import ceil
import os
import sys
import pandas as pd
import numpy as np
from typhon import Typhon
typhon = Typhon()

def gen_embed(data):
    # model, data = args
    print(f'data type in get_embed = {type(data)}')
    embedding = typhon.generate_embedding(data)
    return embedding

if __name__ == '__main__':
    model = typhon
    number = 3

    try :
        if (sys.argv[1]):
            number = sys.argv[1]
            print(f"'argv 1 = {number}")
    except:
        print(f"argv 1 = {number} by default")

    if 'test-embedding-csv.csv' in os.listdir():
        os.remove('test-embedding-csv.csv')

    if not ('typhon-preprocess-to-csv.csv' in os.listdir()):
        df = pd.read_csv('./markdown-index.csv')
        data = df['markdown_content']
        model.preprocess_to_csv(data)
    df = pd.read_csv('./typhon-preprocess-to-csv.csv')

    # print(f'number type  = {type(number)}')
    data = df['preprocessed_markdown'].loc[:int(number)]
    
    partition_number = multiprocessing.cpu_count()
    partition_size = ceil(data.shape[0]/partition_number) if data.shape[0]/partition_number > 1 else 1
    partitions = [data[i:i+partition_size] for i in range(0, len(data), partition_size)]
    # print(f"data.shape = {data.shape}")
    
    # num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=partition_number)
    print(f'len partitions = {len(partitions)}')

    # print(f'partition type = {type(partitions[0][0])}')
    # print(partitions[0][0])
    embeddings = pool.map(gen_embed, partitions)

    final_result = [item for sublist in embeddings for item in sublist]

    pool.close()
    pool.join()

    print(len(final_result))

    df2 = pd.DataFrame({'original': data, 'embeddings': final_result})
    df2.to_csv('embedding-csv-result.csv')
    # print(len(embeddings))
