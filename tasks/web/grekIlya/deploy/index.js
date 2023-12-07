
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const bot = require('./bot');
const Recaptcha = require('express-recaptcha').RecaptchaV2;
const recaptcha = new Recaptcha(process.env.CAPTCHA, process.env.CAPTCHA_SECRET);

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));
app.post('/bot', recaptcha.middleware.verify, (req, res) => {
    if(!req.body || !req.body.url) 
        return res.send('No url specified');
    bot(req.body.url);
    res.send('Admin will visit your url!');
});
app.listen(process.env.PORT, () => {
  console.log('Server is running on port 3000');
});
