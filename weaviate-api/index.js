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
	// res.send({ greet: 'Hello world' });
	const data = {
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
		data,
	});
});

// // Search with Text
// app.get('/weaviate', (req, res) => {
// 	client.graphql
// 		.get()
// 		.withClassName('Article')
// 		.withFields('markdowns')
// 		.withNearText({
// 			concepts: [req.body.markdown],
// 		})
// 		.do()
// 		.then((response) => {
// 			console.log(response);
// 			res.send(response);
// 		})
// 		.catch((err) => {
// 			console.log(err);
// 		});
// });

// //Search with Vector
// app.get('/weaviatevector', (req, res) => {
// 	client.graphql
// 		.get()
// 		.withClassName('Article')
// 		.withFields('markdowns')
// 		.withNearVector({
// 			vector: [req.body.vector],
// 		})
// 		.do()
// 		.then((response) => {
// 			console.log(response);
// 			res.send(response);
// 		})
// 		.catch((err) => {
// 			console.log(err);
// 		});
// });

app.post('/api/v1/ty', async (req, res) => {
	const nearText = {
		concepts: [req.body.query],
	};

	const fetchedResult = await client.graphql
		.get()
		.withClassName('Code')
		.withNearText(nearText)
		.withFields('code _additional { certainty }')
		.do();

	const code_results = fetchedResult['data']['Get']['Code'].map((item) => ({
		code: item.code,
		score: 10,
	}));

	data = {
		totalHits: 10,
		hits: code_results,
	};
	res.status(200).json(fetchedResult);
});

app.get('/api/v1/ty', async (req, res) => {
	const result = await client.graphql
		.get()
		.withClassName('Code')
		.withFields('code _additional { certainty }')
		.do();
	res.send(result);
});

app.listen(port, () => {
	console.log(`WeaviateAPI app listening on port ${port}!`);
});
