import * as dotenv from 'dotenv';
import express from 'express';
import bodyParser from 'body-parser';
import fetch from 'node-fetch';
import weaviate from 'weaviate-client';

dotenv.config();

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const URI = process.env.ELASTICSEARCH_ADDRESS;
const PREPROCCESS_INDEX = process.env.ELASTICSEARCH_PREPROCESS_INDEX;

const weaviateClient = weaviate.client({
	scheme: 'http',
	host: process.env.WEAVIATE_ADDRESS,
});

app.post('/api/v1/ir/:index', async (req, res) => {
	const isPreprocess = req.params.index === PREPROCCESS_INDEX;

	const baseQuery = {
		query: {
			match: {
				markdown: {
					query: req.body.query,
				},
			},
		},
	};

	const preprocessQuery = {
		query: {
			match: {
				processed: {
					query: req.body.query,
				},
			},
		},
	};

	const url = `${URI}/${req.body.index}/_search?pretty`;
	const elasticRes = await (
		await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-ndjson',
			},
			body: JSON.stringify(isPreprocess ? preprocessQuery : baseQuery),
		})
	).json();

	// error catch
	if (!elasticRes)
		return res.status(500).json({ error: 'Internal server error' });
	if (elasticRes.timed_out) return res.status(400).json({ error: 'Timeout' });
	if (elasticRes.hits.hits.length < 0)
		return res.status(400).json({ error: 'No Result' });

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

app.get('/api/v1/ir', (req, res) => {
	res.status(200).json({ message: 'Typhon: Hello World' });
});

app.get('/api/v1/ml/all', async (req, res) => {
	const className = 'GrandMasterCode';
	const fetchedResult = await weaviateClient.graphql
		.get()
		.withClassName(className)
		.withFields('code _additional { id }')
		.do();

	// error catch
	if (!fetchedResult)
		return res.status(500).json({ error: 'Internal server error' });
	if (fetchedResult['data']['Get'][className].length < 0)
		return res.status(400).json({ error: 'No Result' });

	const codeResults =
		fetchedResult['data']['Get'][className].map((item) => ({
			code: item['code'],
			score: item['_additional']['certainty'],
			id: item['_additional']['id'],
		})) ?? [];

	const filteredResults = codeResults.filter((r) => r.score > 0.5);

	res.status(200).json({
		data: {
			totalHits: filteredResults.length,
			hits: filteredResults,
		},
	});
});

app.post('/api/v1/ml', async (req, res) => {
	const nearText = {
		concepts: [req.body.query],
	};

	let className = '';
	if (req.body.index.toLowerCase() === 'grandmaster')
		className = 'GrandMasterCode';
	else if (req.body.index.toLowerCase() === 'master') className = 'MasterCode';
	else if (req.body.index.toLowerCase() === 'expert') className = 'ExpertCode';
	else className = 'GrandMasterCode';

	const fetchedResult = await weaviateClient.graphql
		.get()
		.withClassName(className)
		.withNearText(nearText)
		.withFields('code _additional { id certainty }')
		.do();

	console.log('className = ', className);
	// error catch
	if (!fetchedResult)
		return res.status(500).json({ error: 'Internal server error' });
	if (fetchedResult['data']['Get'][className].length < 0)
		return res.status(400).json({ error: 'No Result' });

	const codeResults =
		fetchedResult['data']['Get'][className].map((item) => ({
			code: item['code'],
			score: item['_additional']['certainty'],
			id: item['_additional']['id'],
		})) ?? [];

	const filteredResults = codeResults.filter((r) => r.score > 0.5);

	res.status(200).json({
		data: {
			totalHits: filteredResults.length,
			hits: filteredResults,
		},
	});
});

app.get('/api/v1/ml', async (req, res) => {
	res.status(200).json({ message: 'Weaviate: Typhon Hello World' });
});

app.listen(3030, () => {
	console.log('Server is running on port 3030');
});
