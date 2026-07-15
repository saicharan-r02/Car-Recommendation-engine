# 🏎️ Sports Car Recommendation Engine

Sports Car Recommendation Engine is a Machine Learning project built to suggest the perfect high-performance vehicles to users based on their specific performance criteria. By analyzing a comprehensive dataset of sports cars, the system cleans the data and utilizes similarity algorithms to find the closest match to a user's desired specifications.

# Problem Statement

Selecting a sports car involves evaluating multiple factors such as performance, price, and speed, making it a complex decision-making process. Existing platforms rely on manual filtering and do not effectively capture user preferences across these dimensions. This project addresses the problem by developing a machine learning–based recommendation system that analyzes user-defined criteria and identifies the most suitable cars using similarity-based matching.

# 🚀 Key Features

Performance-Based Matching: Suggests cars based on specific user inputs like engine performance, price, and speed criteria.

Automated Data Preprocessing: Includes robust data cleaning scripts to handle missing values and format the raw dataset for accurate analysis.

Algorithm-Driven Suggestions: Utilizes Machine Learning techniques (like Cosine Similarity) to calculate mathematical closeness between different car profiles.

Scalable Logic: Designed using modular Python scripts, making it easy to plug in larger datasets or connect to a web frontend later.

# 🛠️ Tech Stack

Python: The core programming language used for scripting and logic.

Pandas: Used for extensive data manipulation, cleaning, and formatting of the dataset.

Scikit-Learn: The Machine Learning library utilized for calculating similarities and building the recommendation engine.


# 📁 Project Structure
```
Car-Recommendation/
├── backend/
│   ├── node_modules
│   ├── CR-Backend.py
│   ├── server.js
│   ├── Sport car price.csv
│   ├── package.json
│   └── package-lock.json
│
├── frontend/
│   ├── node_modules
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   ├── eslint.config.js
│   ├── package.json
│   └── package-lock.json
│
├── node_modules
├── package.json
├── package-lock.json
├── .gitignore
└── README.md
```

# ⚙️ Installation & Setup

## 1. Clone the Repository

git clone https://github.com/saicharan-o/Car-Recommendation-python.git
cd car-recommendation

## 2. Install Dependencies
Make sure you have Python installed, then install the required data science libraries:

pip install pandas scikit-learn

## 3. Run the System
### First, ensure your data is processed

python src/data_cleaning.py

### Run the recommendation script to see outputs

python src/recommendation_logic.py

# 🧠 How It Works (The Logic)

Data Ingestion: The system loads Sport car price.csv, which contains various attributes of modern sports cars.

Data Cleaning: The pandas library removes null values, standardizes text (e.g., converting strings to lowercase), and prepares numerical columns for calculation.

Feature Vectorization: The car attributes are converted into a mathematical format (vectors) using scikit-learn.

Similarity Calculation: The system calculates the similarity score between the user's requested criteria and the available cars in the dataset.

# OUTPUT

![Sport Car Recommender – Default Interface](<Sport Car Recommender – Default Interface-fig-1.png>)

![Sport Car Recommender – Low Budget Input](<Sport Car Recommender – Low Budget Input-fig-2.png>)

![Sport Car Recommender – High Budget Configuration](<Sport Car Recommender – High Budget Configuration-fig-3.png>)

![Sport Car Recommender – Recommendation Loading State](<Sport Car Recommender – Recommendation Loading State-fig-4.png>)

![Sport Car Recommender – Recommended Cars Results Page](<Sport Car Recommender – Recommended Cars Results Page-fig-5.png>)

![High Budget Input State](<High Budget Input State-fig-6.png>)

![Luxury Supercar Results](<Luxury Supercar Results-fig-7.png>)

![Low Budget Input State](<Low Budget Input State-fig-8.png>)

![Affordable Sports Car Results](<Affordable Sports Car Results-fig-9.png>)
