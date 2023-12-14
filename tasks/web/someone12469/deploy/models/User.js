const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  username: { type: String, unique: true, required: true },
  password: {type: String, required: true},
  logo: String,
  background: String,
  verified: { type: Boolean, default: false },
  sharedNotes: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Note' }],
});
 
userSchema.pre('save', async function (next) {
    const user = this;
    if (!user.isModified('password')) return next();
  
    const hashedPassword = await bcrypt.hash(user.password, 10);
    user.password = hashedPassword;
    next();
  });
  
module.exports = mongoose.model('User', userSchema);
