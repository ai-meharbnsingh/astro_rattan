const express = require('express');
const router = express.Router();
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

// Get remedies for a kundli
router.get('/:kundliId', auth, async (req, res) => {
  try {
    const kundliId = req.params.kundliId;

    // Verify kundli belongs to user
    const [kundlis] = await db.query(
      'SELECT id FROM kundlis WHERE id = ? AND user_id = ?',
      [kundliId, req.userId]
    );

    if (kundlis.length === 0) {
      return res.status(404).json({ success: false, message: 'Kundli not found' });
    }

    // Get planetary positions
    const [positions] = await db.query(
      'SELECT * FROM planetary_positions WHERE kundli_id = ?',
      [kundliId]
    );

    // Get remedies for each planet position
    const remedies = [];
    for (const pos of positions) {
      const [remedyData] = await db.query(
        'SELECT * FROM remedies_master WHERE planet = ? AND (house = ? OR house IS NULL)',
        [pos.planet, pos.house]
      );
      
      if (remedyData.length > 0) {
        remedies.push({
          planet: pos.planet,
          house: pos.house,
          zodiac_sign: pos.zodiac_sign,
          remedies: remedyData
        });
      }
    }

    res.json({ success: true, remedies });
  } catch (error) {
    console.error('Remedies fetch error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get remedies for specific planet
router.get('/planet/:planet', auth, async (req, res) => {
  try {
    const planet = req.params.planet;
    const validPlanets = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu'];
    
    if (!validPlanets.includes(planet)) {
      return res.status(400).json({ success: false, message: 'Invalid planet' });
    }

    const [remedies] = await db.query(
      'SELECT * FROM remedies_master WHERE planet = ?',
      [planet]
    );

    res.json({ success: true, planet, remedies });
  } catch (error) {
    console.error('Planet remedies fetch error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get all remedies (admin only)
router.get('/all/list', auth, async (req, res) => {
  try {
    const [remedies] = await db.query('SELECT * FROM remedies_master ORDER BY planet, house');
    res.json({ success: true, remedies });
  } catch (error) {
    console.error('All remedies fetch error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
