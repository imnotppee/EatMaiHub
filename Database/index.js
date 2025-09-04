// backend/index.js
const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const bcrypt = require('bcrypt');

const app = express();
const port = 4000;

// Middleware
app.use(cors());
app.use(express.json());

// PostgreSQL
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'Eat_Mai_Hub',
  password: '1234',
  port: 5432,
});

// ✅ API: Register
app.post('/register', async (req, res) => {
  const { user_name, password, user_mail } = req.body;
  console.log('✅ ได้รับข้อมูล:', user_name, user_mail);

  try {
    const hashedPassword = await bcrypt.hash(password, 10);

    const result = await pool.query(
      'INSERT INTO users (user_name, password, user_mail) VALUES ($1, $2, $3) RETURNING *',
      [user_name, hashedPassword, user_mail]
    );

    res.status(201).json({ message: '✅ สมัครสมาชิกสำเร็จ', user: result.rows[0] });
  } catch (err) {
    console.error('❌ Error register:', err);
    res.status(500).json({ message: 'เกิดข้อผิดพลาดในการสมัคร' });
  }
});

// ✅ API: Login
app.post('/login', async (req, res) => {
  const { user_mail, password } = req.body;

  try {
    const result = await pool.query('SELECT * FROM users WHERE user_mail = $1', [user_mail]);

    if (result.rows.length === 0) {
      return res.status(401).json({ message: '❌ ไม่พบผู้ใช้งานนี้' });
    }

    const user = result.rows[0];
    const match = await bcrypt.compare(password, user.password);

    if (match) {
      res.json({ message: '✅ เข้าสู่ระบบสำเร็จ', userId: user.user_id });
    } else {
      res.status(401).json({ message: '❌ รหัสผ่านไม่ถูกต้อง' });
    }
  } catch (err) {
    console.error('❌ Error login:', err);
    res.status(500).json({ message: 'เกิดข้อผิดพลาดในเซิร์ฟเวอร์' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`🚀 Backend รันอยู่ที่ http://localhost:${port}`);
});

app.get('/test-db', async (req, res) => {
  try {
    const result = await pool.query("INSERT INTO users (user_name, password, user_mail) VALUES ('dbtest','1234','db@test.com') RETURNING *");
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'DB Error' });
  }
});
