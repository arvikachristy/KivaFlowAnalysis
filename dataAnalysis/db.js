const {Client} = require('pg');

async function insert(data) {
  const client = getClient();
  await client.connect();

  await client.query("INSERT INTO insights (number_of_important_lenders) VALUES ($1);", [data]);

  await client.end();
}

async function select() {
  const client = getClient();
  await client.connect();

  let res
  try {
    res = await client.query("SELECT * FROM data;");
  } catch (err) {
    res = {rows: []}
  }

  await client.end();

  return res.rows
}

async function setup() {
  const client = getClient();
  await client.connect();

  await client.query("CREATE TABLE IF NOT EXISTS insights (timestamp timestamp default current_timestamp, number_of_important_lenders integer);");

  await client.end();
}

function getClient() {
  return new Client({
    database: "postgres",
    host: "postgres",
    user: "postgres",
  });
}

module.exports = {
  insert: insert,
  select: select,
  setup: setup,
};
