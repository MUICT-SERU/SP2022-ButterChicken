from fastapi import FastAPI
from typhon import Typhon

app = FastAPI()
model = Typhon()
number = 3

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/preprocess/{markdown}")
def preprocess(markdown):
    mk = [markdown]
    data = model.preprocess(mk)
    print(data)
    return data[0]


@app.get("/embedding/{markdown}")
def embedding(markdown):
    mk = [markdown]
    data = model.generate_embedding(mk)
    print(data)
    return data[0]