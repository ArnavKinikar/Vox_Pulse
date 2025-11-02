const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const path = require('path');

const app = express();
const IPV4_Adress = "10.21.110.16"
const PORT = 5000;

// Enable CORS for Flutter
app.use(cors());
app.use(express.json());

// Serve static audio files from the "audio" folder
app.use('/audio', express.static(path.join(__dirname, 'audio')));

// MySQL Connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'voxpulse'
});

db.connect(err => {
  if (err) {
    console.error('❌ MySQL connection failed:', err);
    return;
  }
  console.log('✅ Connected to MySQL Database');
});

// -----------------------------
// API ROUTES
// -----------------------------

// Get all audio records
app.get('/api/audio', (req, res) => {
  const query = 'SELECT * FROM news_items ORDER BY time_created DESC';
  db.query(query, (err, results) => {
    if (err) {
      console.error('Error fetching audio data:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    const updatedResults = results.map(item => {
      let fileName = item.audio_file_path;

      // Only add the /audio prefix (not duplicate full paths)
      const fileUrl = fileName
        ? `http://${IPV4_Adress}:${PORT}/audio/${encodeURIComponent(fileName)}`
        : null;

      return {
        ...item,
        audio_file_path: fileUrl
      };
    });

    if (updatedResults.length > 0) {
      console.log('✅ Sample audio URL:', updatedResults[0].audio_file_path);
    }

    res.json(updatedResults);
  });
});



// Get a specific audio record by ID
app.get('/api/audio/:id', (req, res) => {
  const audioId = req.params.id;
  const query = 'SELECT * FROM news_items WHERE id = ?';
  db.query(query, [audioId], (err, results) => {
    if (err) {
      console.error('Error fetching audio record:', err);
      return res.status(500).json({ error: 'Database error' });
    }
    if (results.length === 0) {
      return res.status(404).json({ error: 'Audio not found' });
    }

    const item = results[0];
    item.audio_file_path = `http://${IPV4_Adress}:${PORT}/audio/${encodeURIComponent(item.audiofilepath)}`;
    res.json(item);
  });
});

// Root route (optional)
app.get('/', (req, res) => {
  res.send('✅ VoxPulse Audio API is running. Use /api/audio to see the data.');
});

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Server running at: http://${IPV4_Adress}:${PORT}`);
});
