from fastapi import FastAPI, Response, status
import os
from typhon_lite import Typhon
app = FastAPI()

model = Typhon()

from pydantic import BaseModel

class VectorInput(BaseModel):
    text: str


@app.get("/.well-known/live", response_class=Response)
@app.get("/.well-known/ready", response_class=Response)
def live_and_ready(response: Response):
    response.status_code = status.HTTP_204_NO_CONTENT


@app.get("/meta")
def meta():
    # return meta_info.get()
    return {
        "name": "Typhon",
        "lang": "en"
    }


@app.post("/vectors")
async def read_item(item: VectorInput, response: Response):
    try:
        vector = model.embedding([item.text])
        return {"text": item.text, "vector": vector, "dim": len(vector)}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
