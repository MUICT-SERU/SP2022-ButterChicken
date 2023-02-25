from fastapi import FastAPI
from typhon import Typhon
from pydantic import BaseModel

app = FastAPI()
model = Typhon()
number = 3

class Markdown(BaseModel):
    markdown: list

# preprcess api
@app.get("/preprocess")
def preprocess(markdown: str):
    # convert string to list
    mk = [markdown]
    # preprocess markdown
    data = model.preprocess(mk)
    #print(data)
    return data[0]

# embedding api
@app.get("/embedding")
def embedding(markdown: str):
    # convert string to list
    mk = [markdown]
    # embedding markdown
    data = model.generate_embedding(mk)
    #print(data)
    return data[0]

# preprcess api with json
@app.post("/preprocessjson/")
def preprocessJSON(md: Markdown):
    # preprocess markdown
    data = model.preprocess(md.markdown)
    return data[0]

# embedding api with json
@app.post("/embeddingjson/")
def embeddingJSON(md: Markdown):
    # embedding markdown
    data = model.generate_embedding(md.markdown)
    return data[0]
    