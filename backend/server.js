const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const path = require('path');

const app = express();

app.use(cors());
app.use(express.json());
app.post('/api/recommend', (req, res) => {

    const { time, price } = req.body;
    const scriptPath = path.join(__dirname, 'CR-Backend.py');
    const python = spawn('python', [scriptPath, time, price]);
    let output = "";
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error("Python Error:", data.toString()));

    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } 
        catch (e) {
            res.json([]);
        }
    });
});

const PORT = 5001;
app.listen(PORT, () => console.log(`Backend running on Port ${PORT}`));