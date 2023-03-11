import * as dotenv from "dotenv";
import express from "express";
import bodyParser from "body-parser";
import fetch from "node-fetch";
import weaviate from "weaviate-client";

dotenv.config();

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const URI = process.env.elasticSearchAddress;
const INDEX = process.env.elasticSearchIndex;
const PREPROCCESS_INDEX = process.env.preprocessIndex;

const weaviateClient = weaviate.client({
  scheme: "http",
  host: process.env.weaviateAddress,
});

app.post("/api/v1/ir/:index", async (req, res) => {
  const requestIndex =
    req.params.index === PREPROCCESS_INDEX ? PREPROCCESS_INDEX : INDEX;

  const info = {
    query: {
      match: {
        markdown: {
          query: req.body.query,
        },
      },
    },
  };

  const url = `${URI}/${requestIndex}/_search?pretty`;
  const elasticRes = await (
    await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-ndjson",
      },
      body: JSON.stringify(info),
    })
  ).json();

  // error catch
  if (!elasticRes)
    return res.status(500).json({ error: "Internal server error" });
  if (elasticRes.timed_out) return res.status(400).json({ error: "Timeout" });
  if (elasticRes.hits.hits.length < 0)
    return res.status(400).json({ error: "No Result" });

  res.status(200).json({
    data: {
      totalHits: elasticRes.hits.total.value,
      hits: elasticRes.hits.hits.map((hit) => ({
        code: hit._source.code,
        score: hit._score,
      })),
    },
  });
});

app.get("/api/v1/ir", (req, res) => {
  res.status(200).json({ message: "Typhon: Hello World" });
});

app.get("/api/v1/ml/all", async (req, res) => {
  const fetchedResult = await weaviateClient.graphql
    .get()
    .withClassName("Code")
    .withFields("code _additional { id }")
    .do();

  // error catch
  if (!fetchedResult)
    return res.status(500).json({ error: "Internal server error" });
  if (fetchedResult["data"]["Get"]["Code"].length < 0)
    return res.status(400).json({ error: "No Result" });

  const code_results =
    fetchedResult["data"]["Get"]["Code"].map((item) => ({
      code: item["code"],
      score: item["_additional"]["certainty"],
      id: item["_additional"]["id"],
    })) ?? [];

  const data = {
    totalHits: code_results.length,
    hits: code_results,
  };
  res.status(200).json(data);
});

app.post("/api/v1/ml", async (req, res) => {
  const nearText = {
    concepts: [req.body.query],
  };

  const fetchedResult = await weaviateClient.graphql
    .get()
    .withClassName("Code")
    .withNearText(nearText)
    .withFields("code _additional { id certainty }")
    .do();

  // error catch
  if (!fetchedResult)
    return res.status(500).json({ error: "Internal server error" });
  if (fetchedResult["data"]["Get"]["Code"].length < 0)
    return res.status(400).json({ error: "No Result" });

  const code_results =
    fetchedResult["data"]["Get"]["Code"].map((item) => ({
      code: item["code"],
      score: item["_additional"]["certainty"],
      id: item["_additional"]["id"],
    })) ?? [];

  const data = {
    totalHits: code_results.length,
    hits: code_results,
  };
  res.status(200).json(data);
});

app.get("/api/v1/ml", async (req, res) => {
  res.status(200).json({ message: "Weaviate: Typhon Hello World" });
});

app.listen(3030, () => {
  console.log("Server is running on port 3030");
});
