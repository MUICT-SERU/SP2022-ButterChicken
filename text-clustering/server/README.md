# Tyhpon Server

API documetations are also available [here](http://127.0.0.1:8000/docs) when the server is running.

# GET

## Preprocess

`GET /preprocess/{markdown}`

## Response

    "preprocessed markdown"

### Embedding

`GET /embedding/{markdown}`

## Response

    [embedded markdown]

# POST

Use `JSON file` as input.

## Preprocess with JSON

`POST /preprocessjson/`

### Request

    {
        "markdown": ["markdown"]
    }

### Response

    "preprocessed markdown"

## Embedding with JSON

`POST /embeddingjson/`

### Request

    {
        "markdown": ["markdown"]
    }

### Response

    [embedded markdown]
