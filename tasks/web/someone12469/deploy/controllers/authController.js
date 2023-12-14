const bcrypt = require('bcrypt');
const User = require('../models/User');

exports.register = async (req, res) => {
    const { username, password } = req.body;
    console.log(username, password)
    try {
      const user = new User({ username, password });
      await user.save();
      res.redirect("/auth/login");
    } catch (error) {
      res.status(500).json({ error: 'Registration failed' });
    }
};

exports.login = async (req, res) => {
    const { username, password } = req.body;
    console.log(username, password)
    try {
      const user = await User.findOne({ username });
  
      if (!user || !await bcrypt.compare(password, user.password)) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }
      req.session.user = user;
      res.redirect("/");
    } catch (error) {
      res.status(500).json({ error: 'Login failed' });
    }
};
