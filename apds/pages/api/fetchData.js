// pages/api/fetchData.js
import db from '../db.js';

export default async (req, res) => {
  try {
    const [rows] = await db.promise().query('SELECT * FROM events');
    res.status(200).json(rows);
  } catch (error) {
    console.error('Error fetching data:', error);
    res.status(500).json({ error: 'Unable to fetch data' });
  }
};

