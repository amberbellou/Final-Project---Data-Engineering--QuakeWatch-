# 🌍 QuakeWatch — Real-time Earthquake Data Pipeline & Dashboard

QuakeWatch is a data engineering project that ingests, processes, and visualizes earthquake data in near real time.  
It fetches seismic event data from the **USGS Earthquake API**, processes and validates it, stores it in a database, exposes it via a **FastAPI service**, and provides an interactive **Streamlit dashboard** for exploration.

---

## 📖 Project Overview

QuakeWatch is a real-time earthquake monitoring system that collects, processes, and visualizes global seismic activity.  
The goal is to provide a clean, structured dataset and a live dashboard for researchers, analysts, and the public to track earthquakes as they happen.

The pipeline runs automatically every **6 hours** to keep the data fresh.  
This project was designed to demonstrate a full ETL lifecycle, automation with cron, and modern visualization techniques.

---

## 🎯 Purpose and Use Cases
QuakeWatch is useful for:
- 🧑‍🔬 Researchers studying seismic trends over time.  
- 🏛️ Governments & disaster-response teams monitoring earthquake activity.  
- 🎓 Educators and students learning about seismology and data pipelines.  
- 🌍 Anyone curious about real-time global earthquake activity.  

---

## 📌 System Architecture

### 1. ETL Pipeline
- **Extract**: Pulls earthquake event data from the USGS feed.  
- **Transform**: Cleans and validates the data (e.g., country parsing, Pandera schema checks).  
- **Load**: Stores processed events into a local **SQLite database** (PostgreSQL ready).  

### 2. API (FastAPI)
- REST endpoints for:
  - Recent earthquake events  
  - Statistics by country  
  - Service health checks  
- Auto-documented with Swagger UI at **`/docs`**.  

### 3. Dashboard (Streamlit)
- Interactive web app for real-time insights.  
- Includes:
  - 🌎 Map of events  
  - 📊 Magnitude timeline  
  - 📋 Recent events table  
  - 🏆 Top countries by quake count  
  - Filters for magnitude thresholds and row limits.  

---

## 🛠 Tech Stack

| Component       | Technology                                                         |
| --------------- | ------------------------------------------------------------------ |
| Data Source     | [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/) |
| Database        | SQLite (local) / PostgreSQL (optional)                             |
| API             | FastAPI                                                            |
| Dashboard       | Streamlit                                                          |
| Orchestration   | Cron (local) / Prefect (optional)                                  |
| Language        | Python 3.11                                                        |
| ORM             | SQLAlchemy                                                         |
| Data Processing | Pandas + Pandera                                                   |

---

## 📂 Project Structure

Final-Project---Data-Engineering--QuakeWatch-/

├── app/ # API & Dashboard code

│ ├── api.py # FastAPI service

│ ├── dashboard.py # Streamlit dashboard

│ ├── db.py # Database connection

│ └── models.py # ORM models

│

├── etl/ # ETL pipeline code

│ ├── extract.py # Fetch data

│ ├── transform.py # Clean & validate

│ ├── load.py # Load into DB

│ └── flow.py # Orchestration

│

├── templates/ # HTML templates

│ └── events.html

│

├── tests/ # Unit tests

│ ├── test_api.py

│ └── test_transform.py

│

├── requirements.txt # Python dependencies

├── docker-compose.yml # Optional multi-service setup

├── Makefile # Automation commands

├── local.db # Local SQLite DB

├── etl_cron.log # Logs from cron runs

└── README.md # Documentation



---
## 📸 Screenshots

### API Swagger UI
![Swagger UI](https://github.com/user-attachments/assets/ee5f71e5-c78d-4d51-95a9-3486f1ba38d0)

### API Health Check
![Health Check](https://github.com/user-attachments/assets/5cd99f0c-d48a-4821-ad54-0a706c6aa363)

### JSON Events Endpoint
![Events JSON](https://github.com/user-attachments/assets/937d4601-32ea-4fe0-8769-efca7817af55)

### Stats by Country Endpoint
![Stats by Country](https://github.com/user-attachments/assets/193a7068-ffc5-4082-88ec-d6de095ecf22)

### Dashboard – Top Countries by Quake Count
![Dashboard by Country](https://github.com/user-attachments/assets/1d7a759b-3974-46f2-a732-4177036abb84)

### Dashboard – Recent Trends
![Recent Trends](https://github.com/user-attachments/assets/a969d52e-0cf2-4e91-893e-b82236c418f2)

### Dashboard – World Map
![Global Map](https://github.com/user-attachments/assets/66908318-8de1-431b-b511-ec1235d3dc2d)

---

## 🚀 How to Run Locally

```bash
# 1️⃣ Clone the repository
git clone https://github.com/<yourusername>/quakewatch.git
cd quakewatch

# 2️⃣ Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run ETL manually
DATABASE_URL=sqlite:///./local.db python -m etl.flow

# 5️⃣ Start API (port 8001)
uvicorn app.api:app --reload --port 8001

# 6️⃣ Start Dashboard (port 8505)
streamlit run app/dashboard.py --server.port 8505

# 7️⃣ Verify cron job
crontab -l

📊 Example API Calls

# Health check
curl http://localhost:8001/health

# Recent events
curl -s "http://localhost:8001/events.json?min_mag=4&limit=3" | jq .

# Stats by country
curl -s "http://localhost:8001/stats/by-country?min_mag=5" | jq .

#

✅ Features

Automated ETL pipeline (runs every 6 hours).
Database-backed API for structured earthquake data.
Interactive Streamlit dashboard with maps, charts, and filters.
Cron-based scheduling with logs.
Modular, extensible design for future scaling.

📅 Future Improvements

Historical trend analysis.
Advanced filtering (date ranges, depth).
Real-time alerts for major events.
Deployment to cloud (AWS/GCP/Render).

👩‍💻 Author
Developed by Amber Bellou
This project was built as my Data Engineering final project, combining ETL, APIs, and dashboards into a single, automated pipeline.
