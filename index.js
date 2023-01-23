import express from 'express';
import bodyParser from 'body-parser';
import fetch from 'node-fetch';

const app = express();

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }));

const URI = 'http://docker40937-typhon-server.th1.proen.cloud:9200'
const INDEX = 'pre-eva'

app.post('/api/v1/ir', async (req, res) => {

  const info = {
    query: {
      match: {
        markdown: {
          query: req.body.query,
        }
      }
    }
  }

  const url = `${URI}/${INDEX}/_search?pretty`
  const elasticRes = await (await fetch(url, {
    method: "POST",
    headers: {
      'Content-Type': 'application/x-ndjson'
    },
    body: JSON.stringify(info)
  })).json();
  
  // error catch
  if (!elasticRes) return res.status(500).json({ error: 'Internal server error' });
  if (elasticRes.timed_out) return res.status(400).json({ error: 'Timeout' });
  if (elasticRes.hits.hits.length < 0) return res.status(400).json({ error: 'No Result' });

  res.status(200).json({
    data: {
      totalHits: elasticRes.hits.total.value,
      hits: elasticRes.hits.hits.map((hit) => ({
        code: hit._source.code,
        score: hit._score,
      }))
    }
  });
});

app.get('/api/v1/ir', (req, res) => {
  res.status(200).json({ message: 'Hello World' });
});

app.listen(3030, () => {
  console.log('Server is running on port 3030');
});