const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const db = require('../database/connection');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'lalkitabsecretkey';

// Authentication middleware
const auth = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    if (!token) {
      return res.status(401).json({ success: false, message: 'No token, authorization denied' });
    }

    const decoded = jwt.verify(token, JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch (error) {
    res.status(401).json({ success: false, message: 'Token is not valid' });
  }
};

// Calculate planetary positions (simplified calculation)
const calculatePlanetaryPositions = (dateOfBirth, timeOfBirth, latitude, longitude) => {
  // This is a simplified placeholder. In production, use Swiss Ephemeris or similar
  const planets = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu'];
  const zodiacSigns = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'];
  
  const positions = [];
  
  planets.forEach((planet, index) => {
    // Simplified calculation - in production use proper ephemeris
    const house = ((index + 1) % 12) + 1;
    const signIndex = (index + 2) % 12;
    const degree = (index * 15) % 30;
    
    positions.push({
      planet,
      house,
      zodiac_sign: zodiacSigns[signIndex],
      degree: degree.toFixed(2),
      is_retrograde: index % 3 === 0
    });
  });
  
  return positions;
};

// Create new Kundli
router.post('/create', auth, [
  body('name').notEmpty().withMessage('Name is required'),
  body('date_of_birth').isDate().withMessage('Valid date of birth is required'),
  body('time_of_birth').notEmpty().withMessage('Time of birth is required'),
  body('place_of_birth').notEmpty().withMessage('Place of birth is required'),
  body('gender').isIn(['male', 'female', 'other']).withMessage('Gender is required'),
  body('latitude').optional().isFloat(),
  body('longitude').optional().isFloat()
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, errors: errors.array() });
    }

    const { name, date_of_birth, time_of_birth, place_of_birth, gender, latitude, longitude } = req.body;
    const userId = req.userId;

    // Create kundli record
    const [kundliResult] = await db.query(
      'INSERT INTO kundlis (user_id, name, date_of_birth, time_of_birth, place_of_birth, latitude, longitude, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
      [userId, name, date_of_birth, time_of_birth, place_of_birth, latitude, longitude, gender]
    );

    const kundliId = kundliResult.insertId;

    // Calculate and store planetary positions
    const positions = calculatePlanetaryPositions(date_of_birth, time_of_birth, latitude, longitude);
    
    for (const pos of positions) {
      await db.query(
        'INSERT INTO planetary_positions (kundli_id, planet, house, zodiac_sign, degree, is_retrograde) VALUES (?, ?, ?, ?, ?, ?)',
        [kundliId, pos.planet, pos.house, pos.zodiac_sign, pos.degree, pos.is_retrograde]
      );
    }

    res.status(201).json({
      success: true,
      message: 'Kundli created successfully',
      kundli_id: kundliId,
      planetary_positions: positions
    });
  } catch (error) {
    console.error('Kundli creation error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get all kundlis for user
router.get('/list', auth, async (req, res) => {
  try {
    const [kundlis] = await db.query(
      'SELECT id, name, date_of_birth, time_of_birth, place_of_birth, gender, created_at FROM kundlis WHERE user_id = ? ORDER BY created_at DESC',
      [req.userId]
    );

    res.json({ success: true, kundlis });
  } catch (error) {
    console.error('Kundli list error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get single kundli with planetary positions
router.get('/:id', auth, async (req, res) => {
  try {
    const kundliId = req.params.id;

    // Get kundli details
    const [kundlis] = await db.query(
      'SELECT * FROM kundlis WHERE id = ? AND user_id = ?',
      [kundliId, req.userId]
    );

    if (kundlis.length === 0) {
      return res.status(404).json({ success: false, message: 'Kundli not found' });
    }

    // Get planetary positions
    const [positions] = await db.query(
      'SELECT * FROM planetary_positions WHERE kundli_id = ? ORDER BY house',
      [kundliId]
    );

    res.json({
      success: true,
      kundli: kundlis[0],
      planetary_positions: positions
    });
  } catch (error) {
    console.error('Kundli fetch error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Delete kundli
router.delete('/:id', auth, async (req, res) => {
  try {
    const kundliId = req.params.id;

    const [result] = await db.query(
      'DELETE FROM kundlis WHERE id = ? AND user_id = ?',
      [kundliId, req.userId]
    );

    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'Kundli not found' });
    }

    res.json({ success: true, message: 'Kundli deleted successfully' });
  } catch (error) {
    console.error('Kundli delete error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
