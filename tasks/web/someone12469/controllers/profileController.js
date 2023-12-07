const Note = require('../models/Note');
const User = require('../models/User');

exports.getUserProfile = async (req, res) => {
    const username  = req.params.username || req.session.user.username;

    try {
      const user = await User.findOne({ username });
      console.log("adsasd",user);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      const notes = await Note.find({username});
      const filtredNotes = []
      if(username != req.session.user.username){
        const sessionUser = await User.findOne({username: req.session.user.username});
        notes.forEach(note => {
          if(!sessionUser.sharedNotes.includes(note._id)){
            note.content = "You don't have access to this note";
          }
          filtredNotes.push(note);
        })
      }
      res.render('profile', {user: user, notes: filtredNotes});
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch user profile' });
    }
};

exports.updateUserProfile = async (req, res) => {
    const { username } = req.session.user;  
    try {
      const user = await User.findOne({  username });
  
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      for (const key in req.body) {
        user[key] = req.body[key];
      }
      await user.save();
      res.json({ message: 'Profile updated successfully' });
    } catch (error) {
      res.status(500).json({ error: 'Failed to update user profile' });
    }
};
