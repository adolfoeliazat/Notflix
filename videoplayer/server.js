const express = require("express");
const app = express();
const port = process.env.PORT || 8080;

app.use(express.static(__dirname));

// app.get("/", (req, res) => {
//   res.sendfile("index.html");
// });

app.listen(port, function () {
  console.log("Notflix started!");
});