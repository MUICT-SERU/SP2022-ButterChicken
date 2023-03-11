from fastapi import FastAPI
from typhon_lite import Typhon
from pydantic import BaseModel

app = FastAPI()
model = Typhon()
number = 3

class Markdown(BaseModel):
    markdown: list

@app.get('/')
def index():
    return {
        "greet": "Hello World"
    }

# preprcess api
@app.get("/preprocess")
def preprocess(markdown: str):
    # preprocess markdown by converting to list 
    data = model.preprocess([markdown])
    # print(data)
    #print(data)
    return {
        'original_markdown': markdown,
        'preprocessed_markdown' : data[0]
        }

# embedding api
@app.get("/embedding")
def embedding(markdown: str):
    # embedding markdown by convert string to list
    data = model.generate_embedding([markdown])
    #print(data)
    return {
        'original_markdown': markdown,
        'generated_embedding' : data[0]
        }

# preprcess api with json
@app.post("/preprocess")
def preprocessJSON(markdown: Markdown):
    # preprocess markdown
    data = markdown.markdown
    result = model.preprocess(data)
    return {
        'original_markdowns': data,
        'preprocessed_markdown' : result
        }

# embedding api with json
@app.post("/embedding")
def embeddingJSON(markdown: Markdown):
    # embedding markdown
    data = markdown.markdown
    result = model.generate_embedding(data)
    return {
        'original_markdowns': data,
        'generated_embeddings' : result
        }
    
