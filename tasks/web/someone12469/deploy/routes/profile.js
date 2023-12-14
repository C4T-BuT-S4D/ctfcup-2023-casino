const express = require('express');
const router = express.Router();
const profileController = require('../controllers/profileController');

router.get('/:username', profileController.getUserProfile);
router.put('/', profileController.updateUserProfile);

module.exports = router;
