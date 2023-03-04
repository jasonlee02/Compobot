const express = require('express')
const app = express()
const port = 3000
require('dotenv').config();
const dynamodb = require('@aws-sdk/client-dynamodb');
const {
  DynamoDBDocumentClient,
  PutCommand,
  ScanCommand,
} = require('@aws-sdk/lib-dynamodb');

const client = new dynamodb.DynamoDBClient({
  region: 'us-east-1',
});
const ddbDocClient = new DynamoDBDocumentClient(client);

//username = id

app.get('/get/:username', async (req, res) => {
  console.log(req.params.username)
  let username = req.params.username
  const cmd = new ScanCommand({
    TableName: "Compobot",
    Key: username
  })
  const response = await ddbDocClient.send(cmd);
  res.json({'money': response.money})
})

app.post('/update/:username/:value', async (req, res) => {
    const cmd = new PutCommand({
        Item: {
          id: req.params.username,
          value: req.params.value
        },
        TableName: 'Compobot',
      });
      await ddbDocClient.send(cmd);
      res.send("Hello!")
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})