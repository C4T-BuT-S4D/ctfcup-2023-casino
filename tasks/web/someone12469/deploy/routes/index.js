const express = require('express');
const router = express.Router();
const authenticateToken = require('../middlewares/authenticateToken');

const authRoutes = require('./auth');
const noteRoutes = require('./notes');
const profileRoutes = require('./profile');
const Note = require('../models/Note');
const User = require('../models/User');

async function home(req,res){
    const {username} = req.session.user;
    const notes = await Note.find({username});
    const user = await User.findOne({username});
    console.log(user);
    user.sharedNotes.forEach(async _id => { 
        notes.push(await Note.findOne(_id));
    });
    console.log(notes);
    res.render('home',{user: req.session.user, notes: notes});
}
router.use('/auth', authRoutes);
router.use('/notes', authenticateToken, noteRoutes);
router.use('/profile', authenticateToken, profileRoutes);
router.use('/',authenticateToken,home);
module.exports = router;
