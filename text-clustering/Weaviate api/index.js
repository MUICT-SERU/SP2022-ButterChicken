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
    host: 'localhost:8080',
});

app.get('/weaviate', (req, res) => {
    client.graphql
        .get()
        .withCLassName('Article')
        .withFields(req.body)
        .do()
        .then(response => {
            console.log(response);
            res.send(response);
        }
        ).catch(err => {
            console.log(err);
        });          
});

app.listen(port, () => {
    console.log(`WeaviateAPI app listening on port ${port}!`)
});