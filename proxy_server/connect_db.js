const { Client } = require('pg');

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

client.connect();

// Create a table to store important app variables
const createTableQuery = `
  CREATE TABLE IF NOT EXISTS app_config (
    id SERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL
  );
`;

// Insert a configuration value
const insertConfigQuery = `
  INSERT INTO app_config (key, value)
  VALUES ($1, $2)
  ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
`;

client.query(createTableQuery)
  .then(() => {
    console.log("Table 'app_config' created successfully (or already exists).");

    // Store the PORT from environment variables
    return client.query(insertConfigQuery, ['PROXY_PORT', process.env.PORT]);
  })
  .then(() => {
    console.log("PROXY_PORT value inserted/updated successfully.");

    // Retrieve and log the stored values
    return client.query('SELECT * FROM app_config;');
  })
  .then(res => {
    console.log("Stored configuration values:");
    console.table(res.rows);
  })
  .catch(err => console.error("Database error:", err))
  .finally(() => client.end());