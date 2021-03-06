var express = require('express'),
  app = express(),
  http = require('http'),
  httpServer = http.Server(app);
var basicAuth = require("express-basic-auth");
app.use(basicAuth({
    users: { 'dvrn': 'dvrn' },
    challenge: true
}));
app.use(express.static(__dirname + '/'));
app.get('/', function(req, res) {
  res.sendfile(__dirname + '/index.html');
});
app.listen(8080);