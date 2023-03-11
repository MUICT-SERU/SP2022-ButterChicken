# Tyhpon Server

## Run server
    python -m uvicorn server:app --reload

API documetations are also available [here](http://127.0.0.1:8000/docs) when the server is running (local).

# GET

## Preprocess

`GET /preprocess/?markdown={markdown}`

## Response

    {
        "original_markdown": "markdown",
        "preprocessed_markdown": "preprocessed markdown"
    }

### Embedding

`GET /embedding/?markdown{markdown}`

## Response

    {
        "original_markdown": "markdown",
        "generated_embedding": "embedded markdown"
    }

# POST

Use `JSON file` as input.

## Preprocess with JSON

`POST /preprocess/`

### Request body

    {
        "markdown": ["markdown"]
    }

### Response

    {
        "original_markdowns": ["markdown"],
        "preprocessed_markdowns": ["preprocessed markdown"]
    }

## Embedding with JSON

`POST /embedding/`

### Request body

    {
        "markdown": ["markdown"]
    }

### Response

    {
        "original_markdowns": ["markdown"],
        "generated_embeddings": ["embedded markdown"]
    }
