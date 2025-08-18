🌍 QuakeWatch — Real-time Earthquake Data Pipeline & Dashboard

QuakeWatch is a data engineering project that ingests, processes, and visualizes earthquake data in near real time.
It fetches seismic event data, stores it in a PostgreSQL database, exposes it via a FastAPI service, and provides an interactive Streamlit dashboard for exploration.

📖 Project Overview

QuakeWatch is a real-time earthquake monitoring system that collects, processes, and visualizes global seismic activity. The goal is to provide a clean, structured dataset and a live dashboard for researchers, analysts, and the public to track earthquakes as they happen.
The system automatically fetches earthquake event data from reliable sources, processes it through a custom ETL (Extract, Transform, Load) pipeline, stores it in a database, and serves it through a modern API. A separate dashboard application presents this data with interactive charts, tables, and maps to make trends and recent activity easy to explore.

🔧 How I Built It

This project was designed from scratch with modularity and scalability in mind:
Data Extraction – A Python ETL script retrieves raw earthquake event data from the USGS API.
Transformation – The raw feed is cleaned, enriched (e.g., adding country info), and validated with Pandera.
Loading – The processed data is stored in a SQLite/PostgreSQL database for persistence and querying.
API Layer – A FastAPI service exposes REST endpoints so other applications can access clean earthquake data.
Dashboard – A Streamlit app visualizes real-time stats, including recent events, magnitude distributions, and country-by-country breakdowns.
Automation – Cron jobs (or Prefect locally) run the ETL pipeline every 6 hours to keep data fresh.

🎯 Purpose and Use Cases
QuakeWatch is useful for:
Researchers studying seismic trends over time.
Governments and disaster-response teams monitoring earthquake activity.
Educators and students learning about seismology and data pipelines.
Anyone curious about real-time global earthquake activity.

📌 System Overview
1. ETL Pipeline
Extract: Pulls earthquake event data from the USGS Earthquake API.
Transform: Cleans and structures the data (e.g., extracting country names from raw place descriptions, validating data ranges).
Load: Stores processed events into a database for analysis.
2. API (FastAPI)
Serves clean, structured earthquake data.
Endpoints for: recent events, stats by country, and health checks.
Fully documented with Swagger UI at /docs.
3. Dashboard (Streamlit)
Interactive web app to explore earthquake data.
Includes charts, maps, and tables with filters for magnitude and limits.

🛠 Tech Stack

| Component       | Technology                                                         |
| --------------- | ------------------------------------------------------------------ |
| Data Source     | [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/) |
| Database        | SQLite (local) / PostgreSQL                                        |
| API             | FastAPI                                                            |
| Dashboard       | Streamlit                                                          |
| Orchestration   | Prefect / Cron                                                     |
| Language        | Python 3.11                                                        |
| ORM             | SQLAlchemy                                                         |
| Data Processing | Pandas + Pandera                                                   |


---

## 📂 Project Structure

Final-Project---Data-Engineering--QuakeWatch-/
├── app/                     # API & Dashboard code
│   ├── api.py               # FastAPI service (REST endpoints)
│   ├── dashboard.py         # Streamlit dashboard UI
│   ├── db.py                # Database connection setup
│   └── models.py            # SQLAlchemy ORM models
│
├── etl/                     # ETL pipeline code
│   ├── extract.py           # Extract: fetch data from USGS API
│   ├── transform.py         # Transform: clean & validate with Pandera
│   ├── load.py              # Load: upsert into database
│   └── flow.py              # Prefect flow orchestration
│
├── tests/                   # Unit tests
│   ├── test_api.py
│   └── test_transform.py
│
├── templates/               # HTML templates (e.g., for API pages)
│   └── events.html
│
├── docker-compose.yml       # (Optional) Multi-service setup
├── Dockerfile.disabled      # Old Dockerfile (disabled for Render native Python)
├── requirements.txt         # Python dependencies
├── Makefile                 # Automation commands (build, run, lint, etc.)
├── LICENSE                  # MIT License
├── README.md                # Project documentation
├── local.db                 # Local SQLite database (for dev/demo)
├── etl_cron.log             # Logs from cron-based ETL runs
└── _backup/                 # Backup copy of earlier structure (Docker-first)
    ├── app/
    ├── etl/
    ├── tests/
    └── docker-compose.yml


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

🚀 How to Run Locally
# 1️⃣ Clone the repository
git clone https://github.com/<yourusername>/quakewatch.git
cd quakewatch

# 2️⃣ Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run ETL manually
DATABASE_URL=sqlite:///./local.db python -m etl.flow

# 5️⃣ Start API
uvicorn app.api:app --reload --port 8000

# 6️⃣ Start Dashboard
streamlit run app/dashboard.py --server.port 8501

# 7️⃣ Verify cron job
crontab -l

📊 Example API Calls

# Health check
curl http://localhost:8000/health

# Recent events
curl -s "http://localhost:8000/events.json?min_mag=4&limit=3" | jq .

# Stats by country
curl -s "http://localhost:8000/stats/by-country?min_mag=5" | jq .


✅ Features

Automated ETL pipeline (every 6 hours)
Database-backed API for structured earthquake data
Interactive dashboard with maps, charts, and filters
Cron-based automation with logs
Modular, extensible codebase

📅 Future Improvements

Historical trend analysis
Advanced filtering (date/depth ranges)
Real-time alerts for major events
Deployment to cloud (AWS/GCP/Azure/Render)

👩‍💻 Author

Developed by Amber Bellou
