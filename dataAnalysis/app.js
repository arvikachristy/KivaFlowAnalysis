const db = require("./db.js");
const learn = require("./learn.js");

async function app() {
  await db.setup();
  const data = await db.select();
  const numberOfImportantLenders = learn(data);
  await db.insert(numberOfImportantLenders);
  await db.select();
}

module.exports = app;
