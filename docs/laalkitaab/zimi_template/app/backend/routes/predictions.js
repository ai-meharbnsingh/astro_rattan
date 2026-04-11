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

// Get Nishaniyan (Signs) for a kundli
router.get('/nishaniyan/:kundliId', auth, async (req, res) => {
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

    // Get nishaniyan for each planet position
    const nishaniyan = [];
    for (const pos of positions) {
      const [nishaniData] = await db.query(
        'SELECT * FROM nishaniyan_master WHERE planet = ? AND house = ?',
        [pos.planet, pos.house]
      );
      
      if (nishaniData.length > 0) {
        nishaniyan.push({
          planet: pos.planet,
          house: pos.house,
          zodiac_sign: pos.zodiac_sign,
          nishanis: nishaniData
        });
      }
    }

    res.json({ success: true, nishaniyan });
  } catch (error) {
    console.error('Nishaniyan fetch error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get Lal Kitab Debts (Rin)
router.get('/debts/:kundliId', auth, async (req, res) => {
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

    // Get debts for planets present in kundli
    const debts = [];
    for (const pos of positions) {
      const [debtData] = await db.query(
        'SELECT * FROM lal_kitab_debts WHERE planet = ?',
        [pos.planet]
      );
      
      if (debtData.length > 0) {
        debts.push({
          planet: pos.planet,
          house: pos.house,
          debts: debtData
        });
      }
    }

    res.json({ success: true, debts });
  } catch (error) {
    console.error('Debts fetch error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get Marriage Predictions
router.get('/marriage/:kundliId', auth, async (req, res) => {
  try {
    const kundliId = req.params.kundliId;

    // Verify kundli belongs to user
    const [kundlis] = await db.query(
      'SELECT * FROM kundlis WHERE id = ? AND user_id = ?',
      [kundliId, req.userId]
    );

    if (kundlis.length === 0) {
      return res.status(404).json({ success: false, message: 'Kundli not found' });
    }

    const kundli = kundlis[0];

    // Get planetary positions
    const [positions] = await db.query(
      'SELECT * FROM planetary_positions WHERE kundli_id = ?',
      [kundliId]
    );

    // Calculate marriage predictions based on positions
    const marriageData = {
      kundli_id: kundliId,
      marriage_age: 25,
      manglik_status: 'non-manglik',
      spouse_details: '',
      compatibility_score: 75,
      predictions: '',
      remedies: ''
    };

    // Check for Manglik dosha (Mars in 1, 2, 4, 7, 8, 12)
    const marsPosition = positions.find(p => p.planet === 'mars');
    if (marsPosition && [1, 2, 4, 7, 8, 12].includes(marsPosition.house)) {
      marriageData.manglik_status = 'manglik';
    }

    // Check Venus for spouse details
    const venusPosition = positions.find(p => p.planet === 'venus');
    if (venusPosition) {
      marriageData.spouse_details = `Spouse will be ${venusPosition.house % 2 === 0 ? 'beautiful and artistic' : 'practical and grounded'}.`;
    }

    // Generate predictions based on 7th house
    const seventhHousePlanet = positions.find(p => p.house === 7);
    if (seventhHousePlanet) {
      marriageData.predictions = `Marriage life will be ${seventhHousePlanet.planet === 'jupiter' ? 'blessed and prosperous' : 'challenging but manageable'}.`;
    }

    marriageData.remedies = '1. Worship Lord Shiva and Parvati. 2. Donate to married women on Fridays.';

    res.json({ success: true, marriage_prediction: marriageData });
  } catch (error) {
    console.error('Marriage prediction error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get Career Predictions
router.get('/career/:kundliId', auth, async (req, res) => {
  try {
    const kundliId = req.params.kundliId;

    // Verify kundli belongs to user
    const [kundlis] = await db.query(
      'SELECT * FROM kundlis WHERE id = ? AND user_id = ?',
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

    // Analyze career based on 10th house and planets
    const tenthHousePlanet = positions.find(p => p.house === 10);
    const sunPosition = positions.find(p => p.planet === 'sun');
    const mercuryPosition = positions.find(p => p.planet === 'mercury');

    const careerData = {
      kundli_id: kundliId,
      suitable_careers: [],
      business_suitability: false,
      job_suitability: true,
      favourable_periods: '',
      challenges: '',
      remedies: ''
    };

    if (tenthHousePlanet) {
      switch (tenthHousePlanet.planet) {
        case 'sun':
          careerData.suitable_careers = ['Government Service', 'Administration', 'Leadership Roles'];
          break;
        case 'mercury':
          careerData.suitable_careers = ['Writing', 'Teaching', 'Communication', 'IT'];
          break;
        case 'jupiter':
          careerData.suitable_careers = ['Teaching', 'Law', 'Spirituality', 'Counseling'];
          break;
        case 'venus':
          careerData.suitable_careers = ['Arts', 'Entertainment', 'Fashion', 'Beauty'];
          break;
        case 'mars':
          careerData.suitable_careers = ['Military', 'Police', 'Engineering', 'Sports'];
          break;
        case 'saturn':
          careerData.suitable_careers = ['Mining', 'Real Estate', 'Agriculture', 'Manufacturing'];
          break;
        default:
          careerData.suitable_careers = ['General Administration', 'Business'];
      }
    }

    careerData.favourable_periods = 'Ages 28-35 and 42-50 are particularly favourable for career growth.';
    careerData.challenges = 'Initial struggles may be present, but persistence will lead to success.';
    careerData.remedies = '1. Worship Lord Vishnu. 2. Feed Brahmins on Wednesdays.';

    res.json({ success: true, career_prediction: careerData });
  } catch (error) {
    console.error('Career prediction error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get Health Predictions
router.get('/health/:kundliId', auth, async (req, res) => {
  try {
    const kundliId = req.params.kundliId;

    // Verify kundli belongs to user
    const [kundlis] = await db.query(
      'SELECT * FROM kundlis WHERE id = ? AND user_id = ?',
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

    const healthData = {
      kundli_id: kundliId,
      general_health: '',
      vulnerable_areas: [],
      chronic_issues: '',
      favourable_periods: '',
      precautions: '',
      remedies: ''
    };

    // Analyze health based on planetary positions
    const sunPosition = positions.find(p => p.planet === 'sun');
    const moonPosition = positions.find(p => p.planet === 'moon');
    const marsPosition = positions.find(p => p.planet === 'mars');
    const saturnPosition = positions.find(p => p.planet === 'saturn');

    if (sunPosition && [6, 8, 12].includes(sunPosition.house)) {
      healthData.vulnerable_areas.push('Heart', 'Eyes', 'Blood Pressure');
    }

    if (moonPosition && [6, 8, 12].includes(moonPosition.house)) {
      healthData.vulnerable_areas.push('Stomach', 'Mental Health', 'Fluids');
    }

    if (marsPosition && [6, 8, 12].includes(marsPosition.house)) {
      healthData.vulnerable_areas.push('Blood', 'Muscles', 'Accidents');
    }

    if (saturnPosition && [6, 8, 12].includes(saturnPosition.house)) {
      healthData.vulnerable_areas.push('Bones', 'Joints', 'Chronic Conditions');
    }

    healthData.general_health = healthData.vulnerable_areas.length > 0 
      ? 'Pay attention to vulnerable areas and maintain regular health checkups.'
      : 'Generally good health is indicated.';

    healthData.precautions = '1. Regular exercise. 2. Balanced diet. 3. Stress management.';
    healthData.remedies = '1. Worship Lord Hanuman. 2. Donate medicines to needy.';

    res.json({ success: true, health_prediction: healthData });
  } catch (error) {
    console.error('Health prediction error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get Wealth Predictions
router.get('/wealth/:kundliId', auth, async (req, res) => {
  try {
    const kundliId = req.params.kundliId;

    // Verify kundli belongs to user
    const [kundlis] = await db.query(
      'SELECT * FROM kundlis WHERE id = ? AND user_id = ?',
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

    const wealthData = {
      kundli_id: kundliId,
      wealth_potential: 'moderate',
      income_sources: [],
      favourable_periods: '',
      investment_advice: '',
      challenges: '',
      remedies: ''
    };

    // Analyze wealth based on 2nd and 11th house
    const secondHousePlanet = positions.find(p => p.house === 2);
    const eleventhHousePlanet = positions.find(p => p.house === 11);
    const jupiterPosition = positions.find(p => p.planet === 'jupiter');
    const venusPosition = positions.find(p => p.planet === 'venus');

    if (jupiterPosition && [1, 2, 5, 9, 10, 11].includes(jupiterPosition.house)) {
      wealthData.wealth_potential = 'excellent';
    } else if (venusPosition && [1, 2, 5, 9, 10, 11].includes(venusPosition.house)) {
      wealthData.wealth_potential = 'good';
    }

    wealthData.income_sources = ['Primary Job/Business', 'Investments', 'Property'];
    wealthData.favourable_periods = 'Ages 30-36 and 50-58 are favourable for wealth accumulation.';
    wealthData.investment_advice = 'Consider long-term investments in real estate and stable stocks.';
    wealthData.challenges = 'Avoid speculative investments and lending money to strangers.';
    wealthData.remedies = '1. Worship Goddess Lakshmi. 2. Donate to charities on Fridays.';

    res.json({ success: true, wealth_prediction: wealthData });
  } catch (error) {
    console.error('Wealth prediction error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
