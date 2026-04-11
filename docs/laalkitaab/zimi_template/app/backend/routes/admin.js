const express = require('express');
const router = express.Router();
const db = require('../database/connection');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const JWT_SECRET = process.env.JWT_SECRET || 'lalkitabsecretkey';

// Admin authentication middleware
const adminAuth = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    if (!token) {
      return res.status(401).json({ success: false, message: 'No token, authorization denied' });
    }

    const decoded = jwt.verify(token, JWT_SECRET);
    
    // Check if user is admin
    const [admins] = await db.query('SELECT * FROM admin_users WHERE id = ?', [decoded.adminId]);
    if (admins.length === 0) {
      return res.status(403).json({ success: false, message: 'Not authorized as admin' });
    }

    req.adminId = decoded.adminId;
    req.adminRole = admins[0].role;
    next();
  } catch (error) {
    res.status(401).json({ success: false, message: 'Token is not valid' });
  }
};

// Admin login
router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;

    const [admins] = await db.query('SELECT * FROM admin_users WHERE username = ?', [username]);
    if (admins.length === 0) {
      return res.status(400).json({ success: false, message: 'Invalid credentials' });
    }

    const admin = admins[0];
    const isMatch = await bcrypt.compare(password, admin.password);
    if (!isMatch) {
      return res.status(400).json({ success: false, message: 'Invalid credentials' });
    }

    const token = jwt.sign({ adminId: admin.id, role: admin.role }, JWT_SECRET, { expiresIn: '1d' });

    res.json({
      success: true,
      message: 'Admin login successful',
      token,
      admin: { id: admin.id, username: admin.username, role: admin.role }
    });
  } catch (error) {
    console.error('Admin login error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get all users
router.get('/users', adminAuth, async (req, res) => {
  try {
    const [users] = await db.query('SELECT id, name, email, phone, created_at FROM users ORDER BY created_at DESC');
    res.json({ success: true, users });
  } catch (error) {
    console.error('Users fetch error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get all kundlis
router.get('/kundlis', adminAuth, async (req, res) => {
  try {
    const [kundlis] = await db.query(`
      SELECT k.*, u.name as user_name, u.email 
      FROM kundlis k 
      JOIN users u ON k.user_id = u.id 
      ORDER BY k.created_at DESC
    `);
    res.json({ success: true, kundlis });
  } catch (error) {
    console.error('Kundlis fetch error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Add nishaniyan
router.post('/nishaniyan', adminAuth, async (req, res) => {
  try {
    const { planet, house, nishani_text, category, severity } = req.body;

    const [result] = await db.query(
      'INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES (?, ?, ?, ?, ?)',
      [planet, house, nishani_text, category || 'general', severity || 'moderate']
    );

    res.json({ success: true, message: 'Nishaniyan added successfully', id: result.insertId });
  } catch (error) {
    console.error('Add nishaniyan error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Add remedy
router.post('/remedy', adminAuth, async (req, res) => {
  try {
    const { planet, house, remedy_text, remedy_type, duration_days, instructions, caution } = req.body;

    const [result] = await db.query(
      'INSERT INTO remedies_master (planet, house, remedy_text, remedy_type, duration_days, instructions, caution) VALUES (?, ?, ?, ?, ?, ?, ?)',
      [planet, house, remedy_text, remedy_type || 'other', duration_days || 43, instructions, caution]
    );

    res.json({ success: true, message: 'Remedy added successfully', id: result.insertId });
  } catch (error) {
    console.error('Add remedy error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

// Get dashboard stats
router.get('/stats', adminAuth, async (req, res) => {
  try {
    const [userCount] = await db.query('SELECT COUNT(*) as count FROM users');
    const [kundliCount] = await db.query('SELECT COUNT(*) as count FROM kundlis');
    const [nishaniyanCount] = await db.query('SELECT COUNT(*) as count FROM nishaniyan_master');
    const [remedyCount] = await db.query('SELECT COUNT(*) as count FROM remedies_master');

    res.json({
      success: true,
      stats: {
        total_users: userCount[0].count,
        total_kundlis: kundliCount[0].count,
        total_nishaniyan: nishaniyanCount[0].count,
        total_remedies: remedyCount[0].count
      }
    });
  } catch (error) {
    console.error('Stats fetch error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
