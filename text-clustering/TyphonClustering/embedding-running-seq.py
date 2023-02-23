import multiprocessing
import os
import sys
import pandas as pd
import numpy as np
from typhon import Typhon
# typhon = Typhon()

# if not ('typhon-preprocess-to-csv.csv' in os.listdir()):
#     df = pd.read_csv('./markdown-index.csv')
#     data = df['markdown_content']
#     typhon.preprocess_to_csv(data)

# df = pd.read_csv('./typhon-preprocess-to-csv.csv')
# data = df['preprocessed_markdown'].loc[:400]

#def gen_embed(args):
#    model, data = args
#    # print(type(data))
#    embedding = model.generate_embedding([data])
#    return embedding[0]

# embeddings = typhon.generate_embedding(data)

# embeddingsfull = typhon.generate_embedding(datafull)
# df2 = pd.DataFrame({'original': data, 'embeddings': embeddings})
# df2.to_csv('test-embedding-csv.csv')
# print(len(embeddings))

if __name__ == '__main__':
    model = Typhon()
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

    print(f'number type  = {type(number)}')
    data = df['preprocessed_markdown'].loc[:int(number)]
    print(f"data.shape = {data.shape}")
    embeddings = model.generate_embedding(data)
    #num_processes = multiprocessing.cpu_count()
    #pool = multiprocessing.Pool(processes=num_processes)
    #print(f'number process = {num_processes}')

    #embeddings = pool.map(gen_embed, [(model, d) for d in data])

    #pool.close()
    #pool.join()

    print(len(embeddings))
    # print(len(embeddings[0]))
    # print(type(embeddings))
    # print(embeddings[0])
    # print(embeddings[0])
    # embeddings = [", ".join(e) for e in embeddings]
    # print("==========================================")

    # print(type(embeddings))
    # embeddings = np.concatenate(embeddings)
    # print(embeddings.shape)

    df2 = pd.DataFrame({'original': data, 'embeddings': embeddings})
    df2.to_csv('test-embedding-csv.csv')
    # print(len(embeddings))
