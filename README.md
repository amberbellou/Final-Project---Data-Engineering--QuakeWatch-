# 🌍 QuakeWatch — Real-time Earthquake Data Pipeline & Dashboard

QuakeWatch is a data engineering project that ingests, processes, and visualizes earthquake data in near real time.  
It fetches seismic event data, stores it in a PostgreSQL database, exposes it via a FastAPI service, and provides an interactive Streamlit dashboard for exploration.

---
📖 Project Overview
QuakeWatch is a real-time earthquake monitoring system that collects, processes, and visualizes global seismic activity. The goal is to provide a clean, structured dataset and a live dashboard for researchers, analysts, and the public to track earthquakes as they happen.
The system automatically fetches earthquake event data from reliable sources, processes it through a custom ETL (Extract, Transform, Load) pipeline, stores it in a database, and serves it through a modern API. A separate dashboard application presents this data with interactive charts, tables, and maps to make trends and recent activity easy to explore.
🔧 How I Built It
This project was designed from scratch with modularity and scalability in mind:
Data Extraction – A Python ETL script retrieves raw earthquake event data from external APIs.
Transformation – The raw feed is cleaned, enriched (e.g., adding country info), and structured for analytics.
Loading – The processed data is stored in a PostgreSQL database for persistence and querying.
API Layer – A FastAPI service exposes REST endpoints so other applications can access clean earthquake data.
Dashboard – A Streamlit app visualizes real-time stats, including recent events, magnitude distributions, and country-by-country breakdowns.
Containerization – Docker Compose orchestrates the ETL, API, and dashboard for easy local or cloud deployment.
🎯 Purpose and Use Cases
QuakeWatch is useful for:
Researchers studying seismic trends over time.
Governments and disaster-response teams monitoring earthquake activity.
Educators and students learning about seismology and data pipelines.
Anyone curious about real-time global earthquake activity.

## 📌 Overview

The system is made up of three main parts:

1. **ETL Pipeline**
   - **Extract**: Pulls earthquake event data from the USGS Earthquake API.
   - **Transform**: Cleans and structures the data (e.g., extracting country names from raw place descriptions, converting data types).
   - **Load**: Stores processed events into a PostgreSQL database for analysis.

2. **API (FastAPI)**
   - Serves clean, structured earthquake data from the database.
   - Provides endpoints for:
     - Recent earthquake events
     - Statistics by country
     - Health checks for service monitoring
   - Fully documented with **Swagger UI** at `/docs`.

3. **Dashboard (Streamlit)**
   - Interactive web app to explore quake trends.
   - Shows:
     - Top countries by quake count
     - Recent events table
     - Magnitude timeline chart
     - Map of quake locations
   - Adjustable filters for magnitude threshold and row limits.

---

## 🛠 Tech Stack

| Component        | Technology |
|------------------|------------|
| Data Source      | [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/) |
| Database         | PostgreSQL 16 (Docker) |
| API              | FastAPI |
| Dashboard        | Streamlit |
| Containerization | Docker + Docker Compose |
| Language         | Python 3.11 |
| ORM              | SQLAlchemy |
| Data Processing  | Pandas |

---

## 📂 Project Structure

quakewatch/
├── app/ # API & Dashboard code
│ ├── api.py # FastAPI endpoints
│ ├── dashboard.py # Streamlit dashboard
│ ├── db.py # DB connection
│ └── models.py # ORM models
├── etl/ # ETL pipeline code
│ ├── extract.py # Data extraction logic
│ ├── transform.py # Data cleaning
│ ├── load.py # Load data into DB
│ └── flow.py # ETL orchestration
├── tests/ # Unit tests
│ ├── test_transform.py # Tests for transforms
│ └── test_api.py # Tests for API
├── docker-compose.yml # Multi-service setup
├── Dockerfile # API/Dashboard container
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .env.example # Sample environment config

---
## Screenshots

### API Swagger UI
Here’s the auto-generated API documentation that lets you test endpoints directly.
![QuakeWatch API Docs](https://github.com/user-attachments/assets/1d7a759b-3974-46f2-a732-4177036abb84)

---

### Dashboard – Top Countries by Quake Count
The dashboard displays the countries with the highest earthquake counts in the dataset.
![Dashboard by Country](https://github.com/user-attachments/assets/a969d52e-0cf2-4e91-893e-b82236c418f2)

---

### Dashboard – Recent Trends
A line chart showing recent earthquake magnitudes over time.
![Recent Trends](https://github.com/user-attachments/assets/66908318-8de1-431b-b511-ec1235d3dc2d)

---

### Dashboard – World Map
Earthquake events plotted on an interactive map.
![Global Map](https://github.com/user-attachments/assets/193a7068-ffc5-4082-88ec-d6de095ecf22)

---

### API Health Check
A simple endpoint to confirm the API is running.
![Health Check](https://github.com/user-attachments/assets/ee5f71e5-c78d-4d51-95a9-3486f1ba38d0)

---

### JSON Events Endpoint
Raw JSON response with recent earthquake data.
![Events JSON](https://github.com/user-attachments/assets/937d4601-32ea-4fe0-8769-efca7817af55)

---

### Stats by Country Endpoint
Aggregated counts of earthquakes by country.
![Stats by Country](https://github.com/user-attachments/assets/5cd99f0c-d48a-4821-ad54-0a706c6aa363)

## 🚀 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<yourusername>/data-engineering.git
cd data-engineering/quakewatch
2️⃣ Set up environment variables
cp .env.example .env
3️⃣ Build and start the services
docker compose up -d --build
This will start:
PostgreSQL on port 5432
FastAPI on port 8000
Streamlit dashboard on port 8501
4️⃣ Access the services
API Docs (Swagger UI) → http://localhost:8000/docs
Dashboard → http://localhost:8501
📊 Example API Calls
Recent events
curl -s "http://localhost:8000/events?min_mag=4&limit=3" | jq .
Stats by country
curl -s "http://localhost:8000/stats/by-country?min_mag=5" | jq .
✅ Features
Automated ETL pipeline to keep data fresh
Database-backed API for clean, structured data
Live dashboard for visual insights
Configurable filters for magnitude and event count
Fully containerized for easy deployment
📅 Future Improvements
Historical trend analysis
Advanced filtering (date range, depth range)
Alerting system for large events
Deployment to cloud (AWS/GCP/Azure)
👩‍💻 Author
Developed by Amber Bellou

