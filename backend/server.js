const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const path = require('path');

const app = express();

app.use(cors());
app.use(express.json());

const SCRIPT_PATH = path.join(__dirname, 'CR-Backend.py');

// 1. Recommendation endpoint
app.post('/api/recommend', (req, res) => {
    const { time, price } = req.body;
    const python = spawn('python', [SCRIPT_PATH, time, price]);
    let output = "";
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error("Python Error:", data.toString()));

    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch (e) {
            res.json([]);
        }
    });
});

// 2. Fetch saved favorites endpoint
app.get('/api/favorites', (req, res) => {
    const python = spawn('python', [SCRIPT_PATH, '--favorites']);
    let output = "";
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error("Python Error:", data.toString()));

    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch (e) {
            res.json([]);
        }
    });
});

// 3. Save favorite endpoint
app.post('/api/favorites', (req, res) => {
    const { car_id, note } = req.body;
    const python = spawn('python', [SCRIPT_PATH, '--save-fav', car_id || 1, note || 'My Favorite']);
    let output = "";
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error("Python Error:", data.toString()));

    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch (e) {
            res.json({ status: "error", error: e.toString() });
        }
    });
});

const PORT = 5001;
app.listen(PORT, () => console.log(`[START] Sports Car Recommender Backend running on Port ${PORT}`));