var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
const katex = require('katex');
var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

// API endpoint to serve flashcard data
app.get('/api/flashcards', (req, res) => {
  let flashcardData = require('./data/flashcards.json');
  
  flashcardData.topics.forEach(topic => {
    topic.cards.forEach(card => {
      // Process question
      card.q = renderMath(card.q);
      // Process answer
      card.a = renderMath(card.a);
    });
  });

  console.log('✅ Flashcards sent with rendered math');
  res.json(flashcardData);
});

function renderMath(text) {
  if (!text) return text;

  // Display math $$...$$
  text = text.replace(/\$\$([^\$]*)\$\$/g, (match, content) => {
    try {
      const rendered = katex.renderToString(content,  { displayMode: false, throwOnError: false, output: 'mathml' });
      return rendered;
    } catch (e) {
      console.warn('KaTeX display error:', e.message);
      return match;
    }
  });

  // Inline math \(...\)
  text = text.replace(/\\\(([^\)]*)\\\)/g, (match, content) => {
    try {
      const rendered = katex.renderToString(content, { displayMode: false, throwOnError: false, output: 'mathml' });
      return rendered;
    } catch (e) {
      console.warn('KaTeX inline error:', e.message);
      return match;
    }
  });

  // Inline math $...$
  text = text.replace(/\$([^\$]+)\$/g, (match, content) => {
    if (content.includes('<span') || content.includes('katex')) return match;
    try {
      content = content.replace(/^[^\\]*?=\s*[^\\$,\n]*,\s*/g, '');
      const rendered = katex.renderToString(content,  { displayMode: false, throwOnError: false, output: 'mathml' }); 
      return rendered;
    } catch (e) {
      console.warn('KaTeX single $ error:', e.message);
      return match;
    }
  });

  return text;
}

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;