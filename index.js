const express = require('express');
const weaviate = require('weaviate-client');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const client = weaviate.client({
	scheme: 'http',
	host: '202.151.177.149:81',
});

app.get('/', (req, res) => {
	const mock_data = {
		totalHits: 10,
		hits: [
			{
				code: 'code',
				score: 11,
			},
			{
				code: 'cod2',
				score: 13,
			},
		],
	};
	res.status(200).json({
		greet: 'Hello world',
		number: 42,
		mock_data,
	});
});

app.post('/api/v1/ty', async (req, res) => {
	const nearText = {
		concepts: [req.body.query],
	};

	const fetchedResult = await client.graphql
		.get()
		.withClassName('Code')
		.withNearText(nearText)
		.withFields('code _additional { id certainty }')
		.do();

	const code_results = fetchedResult['data']['Get']['Code'].map((item) => ({
		code: item['code'],
		score: item['_additional']['certainty'],
		id: item['_additional']['id'],
	}));

	data = {
		totalHits: code_results.length,
		hits: code_results,
	};
	res.status(200).json(data);
});

app.get('/api/v1/ty', async (req, res) => {
	const result = await client.graphql
		.get()
		.withClassName('Code')
		.withFields('code _additional { id }')
		.do();

	const code_results = result['data']['Get']['Code'].map((item) => ({
		code: item['code'],
		score: item['_additional']['certainty'],
		id: item['_additional']['id'],
	}));

	data = {
		totalHits: code_results.length,
		hits: code_results,
	};
	res.status(200).json(data);
});

app.listen(port, () => {
	console.log(`WeaviateAPI app listening on port ${port}!`);
});
