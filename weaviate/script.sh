#!/bin/bash
echo "Start up docker compose"
docker build -f Dockerfile -t text2vec-typhon .
docker compose up
