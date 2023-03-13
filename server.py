from fastapi import FastAPI, HTTPException
from typhon_lite import Typhon
from pydantic import BaseModel
from typing import List

app = FastAPI()
typhon = Typhon()
NUM_MARKDOWNS = 3

class Markdown(BaseModel):
    markdown: List[str]

@app.get('/')
def get_greeting() -> dict:
    return {
        "greet": "Hello World"
    }

# preprocess api
@app.get("/preprocess")
def preprocess(markdown: str) -> dict:
    try:
        data = typhon.preprocess([markdown])
        return {
            'original_markdown': markdown,
            'preprocessed_markdown': data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# embedding api
@app.get("/embedding")
def embedding(markdown: str) -> dict:
    try:
        data = typhon.generate_embedding([markdown])
        return {
            'original_markdown': markdown,
            'generated_embedding': data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# preprocess api with json
@app.post("/preprocess")
def preprocessJSON(markdown: Markdown) -> dict:
    try:
        data = markdown.markdown
        result = typhon.preprocess(data)
        return {
            'original_markdowns': data,
            'preprocessed_markdown': result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# embedding api with json
@app.post("/embedding")
def embeddingJSON(markdown: Markdown) -> dict:
    try:
        data = markdown.markdown
        result = typhon.generate_embedding(data)
        return {
            'original_markdowns': data,
            'generated_embeddings': result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
