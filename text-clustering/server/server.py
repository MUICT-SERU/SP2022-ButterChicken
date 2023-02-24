from fastapi import FastAPI
from typhon import Typhon

app = FastAPI()
model = Typhon()
number = 3

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/preprocess")
async def preprocess():
    model.preprocess()
    return {"message": "Hello World"}


@app.get("/embedding")
async def embedding():
    model.generate_embedding()
    return {"message": "Hello World"}