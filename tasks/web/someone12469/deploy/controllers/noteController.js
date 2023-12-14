const User = require('../models/User');
const Note = require('../models/Note');

exports.createNote = async (req, res) => {
    const { title, content } = req.body;
    const { username } = req.session.user;
    try {
      const user = await User.findOne({ username });
  
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
  
      const newNote = new Note({ title, content, userId: user._id, username: req.session.user.username });
      await newNote.save();
  
      user.sharedNotes.push(newNote._id);
      await user.save();
      const notes = await Note.find({username});
      user.sharedNotes.forEach(async _id => { 
            notes.push(await Note.findOne(_id));
      });
      res.render('home',{user: req.session.user, notes});
    } catch (error) {
      res.status(500).json({ error: 'Failed to create note' });
    }
};

exports.getUserNotes = async (req, res) => {
    const { username } = req.session.user;

    try {
      const user = await User.findOne({ username });
  
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
  
  
      const sharedNotes = user.sharedNotes;
  
      res.render('notes',{notes:sharedNotes.filter(note => note.username.equals(req.params.username)),user:req.session.user});
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch notes' });
    }
};

exports.shareNote = async (req, res) => {
    const { username } = req.body;
    const { noteId } = req.params;
  
    try {
      const userToShareWith = await User.findOne({ username });
      
      if (!userToShareWith) {
        return res.status(404).json({ error: 'User not found' });
      }
  
      const note = await Note.findOne({_id:noteId});
  
      if (!note) {
        return res.status(404).json({ error: 'Note not found' });
      }
  
      if (note.userId.equals(userToShareWith._id)) {
        return res.status(400).json({ error: 'Cannot share a note with its owner' });
      }

      if (!note.userId.equals(note.userId)) {
        return res.status(400).json({ error: 'Cannot share this note' });
      }

      if (!note.sharedWith.some(userId => userId.equals(userToShareWith._id))) {
        note.sharedWith.push(userToShareWith._id);
        await note.save();
  
        userToShareWith.sharedNotes.push(note._id);
        await userToShareWith.save();
      }
  
      res.json({ message: 'Note shared successfully' });
    } catch (error) {
      res.status(500).json({ error: 'Failed to share note' });
    }
};

exports.getPaginatedUserNotes = async (req, res) => {
    const { username } = req.session.user;
    const { page = 1, pageSize = 10 } = req.query;
  
    try {
      const user = await User.findOne({ username });
  
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      res.render('notes',sharedNotes.filter(note => note.username.equals(req.params.username)).slice((page - 1) * pageSize, page * pageSize));
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch paginated notes' });
    }
  };