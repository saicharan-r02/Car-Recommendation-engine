# 🏎️ Sports Car Recommendation Engine & Dynamic Inventory System

Sports Car Recommendation Engine is a Machine Learning and Database-driven project built to suggest the perfect high-performance vehicles based on specific user budget and speed criteria. The system pairs normalized vector distance matching with a dynamic **SQLite / SQLAlchemy** inventory and user wishlist/garage bookmarks.

---

## 🎯 Problem Statement

Selecting a sports car involves evaluating multiple dimensions such as horsepower, 0–60 MPH acceleration time, price, and brand heritage. Existing platforms rely on rigid manual filters. This project solves this by using similarity-based matching over dynamic database records, enabling users to find the closest vehicle matching their performance targets and save their dream cars to a personalized garage wishlist.

---

## 🚀 Key Features

- 🏎️ **Performance-Based Similarity Matching**: Normalizes price and acceleration parameters to compute mathematical closeness scores across sports car models.
- 🗄️ **Dynamic Database & Auto-Seeder (SQLite / SQLAlchemy)**: Automatically parses and seeds 178+ sports cars from CSV on first launch and supports live database queries without modifying code.
- 🚘 **Garage / Wishlist Persistence**: Save and bookmark favorite cars with custom notes directly to the database.
- 📊 **Search Query Logging**: Automatically records user budget and acceleration preferences for analytics.
- 🔌 **REST API Ready**: Express.js server providing `/api/recommend` and `/api/favorites` (GET/POST) endpoints.
- 🎨 **Responsive Frontend**: Modern React + Vite user interface with real-time state management.

---

## 🛠️ Tech Stack

### Frontend:
* **React.js & Vite**
* **Vanilla CSS3** (High-Performance Dark Theme)

### Backend & Machine Learning:
* **Node.js (Express.js)** (API Gateway & Process Orchestration)
* **Python 3** (Data Processing & Similarity Logic)
* **SQLite / SQLCipher & SQLAlchemy 2.0** (`car_inventory.db`)
* **Pandas & NumPy**

---

## 📁 Project Structure

```
Car-Recommendation/
├── backend/
│   ├── database.py             # SQLAlchemy models, auto-seeder & favorites queries
│   ├── CR-Backend.py           # Similarity calculation & CLI routing
│   ├── server.js               # Express.js REST server
│   ├── car_inventory.db        # SQLite database (auto-seeded on startup)
│   ├── Sport car price.csv     # Raw sports car dataset
│   ├── requirements.txt        # Python dependencies (SQLAlchemy, Pandas, Scikit-Learn)
│   ├── package.json
│   └── package-lock.json
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
└── README.md
```

---

## 🗃️ Database Schema & Inspection

The system utilizes an embedded **SQLite / SQLCipher** database ([`car_inventory.db`](file:///c:/Users/saich/OneDrive/Desktop/python/Car-Recommendation/backend/car_inventory.db)):

### Tables:
1. `cars`: Stores sports car specifications (`brand`, `model`, `year`, `horsepower`, `torque`, `zero_to_sixty`, `price_usd`).
2. `user_favorites`: Stores bookmarked vehicles saved to the user's "Garage".
3. `user_search_logs`: Stores search query parameters (`target_time`, `target_budget`, `results_count`).

### How to Check Stored Data:
Run this Python snippet in your terminal:
```bash
python -c "
import sqlite3, pandas as pd
conn = sqlite3.connect('backend/car_inventory.db')
print('=== TOTAL CARS IN DATABASE ===')
print(pd.read_sql_query('SELECT count(*) as total_cars FROM cars;', conn))
print('\n=== SAMPLE CAR INVENTORY ===')
print(pd.read_sql_query('SELECT id, brand, model, horsepower, zero_to_sixty, price_usd FROM cars LIMIT 5;', conn))
print('\n=== SAVED GARAGE FAVORITES ===')
print(pd.read_sql_query('SELECT * FROM user_favorites;', conn))
"
```
Or open `backend/car_inventory.db` in **DB Browser for SQLite** or **VS Code SQLite Viewer**.

---

## 📡 REST API Endpoints

### 1. `POST /api/recommend`
* **Request Payload**:
```json
{
  "time": 3.2,
  "price": 120000
}
```
* **Response**:
```json
[
  {
    "id": 8,
    "Car_Name": "Mercedes-Benz",
    "Car_Model": "AMG GT",
    "Time": 3.8,
    "Price": 118500.0,
    "Horsepower": 523,
    "Year": 2021
  }
]
```

### 2. `GET /api/favorites`
Returns all saved cars from the user's garage.

### 3. `POST /api/favorites`
* **Request Payload**:
```json
{
  "car_id": 8,
  "note": "Dream track day sports car"
}
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/saicharan-r02/Car-Recommendation-engine.git
cd Car-Recommendation
```

### 2. Backend Setup
```bash
cd backend
npm install
pip install -r requirements.txt
node server.js
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

---

## 🖼️ Interface Screenshots

![Sport Car Recommender – Default Interface](<Sport Car Recommender – Default Interface-fig-1.png>)
![Sport Car Recommender – Low Budget Input](<Sport Car Recommender – Low Budget Input-fig-2.png>)
![Sport Car Recommender – High Budget Configuration](<Sport Car Recommender – High Budget Configuration-fig-3.png>)
![Sport Car Recommender – Recommendation Loading State](<Sport Car Recommender – Recommendation Loading State-fig-4.png>)
![Sport Car Recommender – Recommended Cars Results Page](<Sport Car Recommender – Recommended Cars Results Page-fig-5.png>)
![High Budget Input State](<High Budget Input State-fig-6.png>)
![Luxury Supercar Results](<Luxury Supercar Results-fig-7.png>)
![Low Budget Input State](<Low Budget Input State-fig-8.png>)
![Affordable Sports Car Results](<Affordable Sports Car Results-fig-9.png>)

---

## 👨‍💻 Author

Developed by **Sai Charan** — Automotive Machine Learning & Dynamic Recommendation Systems.
