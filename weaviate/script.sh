#!/bin/bash
echo "Import data"
cd ../typhon-markdown-data
. bash
./script.sh

echo "Start up docker compose"
cd ../typhon-2-model
. bash
docker build -f Dockerfile -t text2vec-typhon .
docker compose up
