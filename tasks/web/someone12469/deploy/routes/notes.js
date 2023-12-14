const express = require('express');
const router = express.Router();
const noteController = require('../controllers/noteController');

router.post('/', noteController.createNote);
router.get('/:username', noteController.getUserNotes);
router.post('/share/:noteId', noteController.shareNote);
router.get('/:username/paginated', noteController.getPaginatedUserNotes);

module.exports = router;
