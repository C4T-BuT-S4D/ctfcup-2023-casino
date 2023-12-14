const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const ejs = require('ejs');
const path = require('path');
const routes = require('./routes');
var cookieSession = require('cookie-session')
const User = require('./models/User');
const Note = require('./models/Note');
const app = express();
const bcrypt = require('bcrypt');
const port = 5000;
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieSession({
    name: 'session',
    keys: [process.env.INIT_USER_PASSWORD],
  
    maxAge: 24 * 60 * 60 * 1000
  }))

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true });
async function init(){
  if(await User.findOne({username: process.env.INIT_USER_USERNAME})) return;
  if (process.env.INIT_USER_USERNAME && process.env.INIT_USER_PASSWORD &&
    process.env.INIT_NOTE_TITLE && process.env.INIT_NOTE_CONTENT) {
  const initUser = new User({
    username: process.env.INIT_USER_USERNAME,
    password: process.env.INIT_USER_PASSWORD,
  });
  
  await initUser.save();
  
  const initNote = new Note({
    title: process.env.INIT_NOTE_TITLE,
    content: process.env.INIT_NOTE_CONTENT,
    userId: initUser._id,
  });
  
  await initNote.save();
  }
}
init();
app.use('/', routes);
  
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
