var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index');  // This loads index.jade
});

// Add route for flashcards if missing:
router.get('/flashcards', function(req, res, next) {
  res.render('flashcards');  // This loads flashcards.jade
});


module.exports = router;
