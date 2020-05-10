const express = require("express");
const path = require("path");
const app = express(); 





app.get('/', function (req,res) {

	res.sendFile(path.join(__dirname, "index.html"));

});

console.log("Home Page on port 5000")
app.listen(80);
