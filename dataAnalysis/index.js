const app = require("./app.js");

function main() {
  app().then(() => {
    console.log("SUCCESS");
  }).catch(err => {
    console.error(err);
  });
}

setInterval(main, 5000);
