require('dotenv').config();
const { Client } = require('pg');
const bcrypt = require('bcrypt');

const dbUrl = process.env.DATABASE_URL;

const initialUsers = [
  { userId: 'E1001', password: 'Password123!' },
  { userId: 'E1002', password: 'Password123!' },
  { userId: 'E1003', password: 'Password123!' },
  { userId: 'E1004', password: 'Password123!' },
  { userId: 'admin', password: 'admin' }
];

async function initDB() {
  console.log(`Connecting to database at ${dbUrl}...`);
  const client = new Client({
    connectionString: dbUrl,
  });

  try {
    await client.connect();
    console.log('Connected successfully. Initializing tables...');

    await client.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
      );
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(100) NOT NULL,
        original_name VARCHAR(255) NOT NULL,
        filename VARCHAR(255) NOT NULL,
        filepath TEXT NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    
    console.log('Tables created or already exist.');

    const res = await client.query('SELECT COUNT(*) FROM users');
    if (parseInt(res.rows[0].count) === 0) {
      console.log('Seeding initial users...');
      const saltRounds = 10;
      for (const user of initialUsers) {
        const hash = await bcrypt.hash(user.password, saltRounds);
        await client.query(
          'INSERT INTO users (user_id, password_hash) VALUES ($1, $2)',
          [user.userId, hash]
        );
        console.log(`Inserted user: ${user.userId}`);
      }
      console.log('Seeding complete.');
    } else {
      console.log('Users table already contains data, skipping seeding.');
    }

  } catch (err) {
    console.error('Error initializing database:', err);
  } finally {
    await client.end();
  }
}

initDB();
