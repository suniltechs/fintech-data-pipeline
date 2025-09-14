# Fintech Data Pipeline

A fully automated **daily pipeline** that fetches stock data, stores it in a PostgreSQL database, and generates AI-driven financial insights using Groq (Llama-3 model). This project is designed for fintech or business data analysis and can be deployed on platforms like Railway.  

---

## Table of Contents
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Technologies Used](#technologies-used)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Database Schema](#database-schema)
- [Contributing](#contributing)

---

## Features
- Fetches daily stock data using **Alpha Vantage API**.
- Stores stock data in **PostgreSQL** with automatic conflict handling.
- Generates **summarized insights and actionable recommendations** using Groq LLM (Llama-3.1-8b-instant).
- Fully automated pipeline with modular and maintainable code structure.
- Deployment-ready for cloud platforms like **Railway**.

---

## Project Architecture
```
fintech-data-pipeline/
│
├── scripts/
│ └── init_db.py # Initializes the PostgreSQL database tables
├── src/
│ ├── init.py
│ ├── config.py # (Optional) Configuration file for environment variables
│ ├── pipeline.py # Main pipeline to fetch data and generate insights
│ ├── alpha_vantage_client.py # Fetches stock data from Alpha Vantage
│ ├── openai_client.py # Generates financial insights using Groq LLM
│ └── database.py # Handles database operations
├── venv/ # Python virtual environment
├── .env # Environment variables
├── .gitignore
├── README.md
├── requirements.txt
└── Procfile # Deployment config for Railway
```

---

## Technologies Used
- **Python 3.11+**
- **PostgreSQL** (hosted on Railway)
- **Alpha Vantage API** (stock data)
- **Groq LLM (Llama-3.1)** (AI insights)
- **Python Libraries**:
  - `requests`
  - `python-dotenv`
  - `psycopg2-binary`
  - `groq`
  - `schedule`

---

## Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/suniltechs/fintech-data-pipeline.git
cd fintech-data-pipeline
```
2. **Create and activate a virtual environment**
```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
3. **Install dependencies**
```
pip install -r requirements.txt
```
4. **Create .env file**
```
# Database
DATABASE_URL=postgresql://username:password@host:port/dbname

# Alpha Vantage API
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
ALPHA_VANTAGE_SYMBOL=IBM

# Groq API
GROQ_API_KEY=your_groq_api_key
```
5. **Initialize the database**
```
python scripts/init_db.py
```
## Usage

**Run the main pipeline to fetch stock data and generate AI insights:**
```
python -m src.pipeline
```

**Sample Output:**
```
Starting pipeline execution...
Fetched data for 2025-09-11
Data stored in database
Analyzing data for 2025-09-11
Insights generated and stored
--- Generated Insights ---
Date: 2025-09-11
Symbol: IBM
Summary: ...
Recommendations: ...
Pipeline execution completed
```

## Environment Variables

| Variable                | Description                 |
| ----------------------- | --------------------------- |
| `DATABASE_URL`          | PostgreSQL connection URL   |
| `ALPHA_VANTAGE_API_KEY` | API key to fetch stock data |
| `ALPHA_VANTAGE_SYMBOL`  | Stock symbol (default: IBM) |
| `GROQ_API_KEY`          | API key for Groq LLM        |

## Database Schema

**Table: stock_data**

| Column      | Type        | Description  |
| ----------- | ----------- | ------------ |
| id          | SERIAL      | Primary key  |
| symbol      | VARCHAR(10) | Stock symbol |
| date        | DATE        | Stock date   |
| open        | NUMERIC     | Open price   |
| high        | NUMERIC     | High price   |
| low         | NUMERIC     | Low price    |
| close       | NUMERIC     | Close price  |
| volume      | BIGINT      | Volume       |
| created\_at | TIMESTAMP   | Timestamp    |

**Table: daily_recommendations**

| Column          | Type        | Description                |
| --------------- | ----------- | -------------------------- |
| id              | SERIAL      | Primary key                |
| date            | DATE        | Stock date                 |
| symbol          | VARCHAR(10) | Stock symbol               |
| summary         | TEXT        | LLM-generated summary      |
| recommendations | TEXT        | Actionable recommendations |
| created\_at     | TIMESTAMP   | Timestamp                  |

## Deployment on Railway
- Add Procfile:
```
worker: python -m src.pipeline
```
- Set all environment variables in Railway dashboard.
- Deploy and schedule the worker to run daily.

## Contributing

1. Fork the repository
2. Create a new branch
3. Make changes & commit
4. Create a pull request

## Developer

Developed by [Sunil Sowrirajan](https://www.linkedin.com/in/sunil-sowrirajan-40548826b/)

[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?style=for-the-badge&logo=github)](https://github.com/suniltechs)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sunil-sowrirajan-40548826b/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Website-green?style=for-the-badge)](https://sunilsowrirajan.netlify.app/)

