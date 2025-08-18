## 🌍 QuakeWatch: Real-time Earthquake Data Pipeline and Dashboard

QuakeWatch is a project I built to bring earthquake data to life in a way that is both useful and easy to explore. Every few hours the system goes out to the USGS Earthquake API, which publishes seismic activity from around the world in real time. Instead of leaving the data as raw messy JSON, QuakeWatch cleans it up, validates it, and organizes it into a structured format that can actually be analyzed. The cleaned data is then stored in a database so that past events are not lost and researchers or curious users can look at historical trends alongside the newest quakes.
From there I wanted to make the data easy to access and visualize. That is why I built a FastAPI service that exposes earthquake information through a set of endpoints anyone can use, whether that is to grab raw numbers, check a health status, or fetch detailed statistics by country. On top of the API I created a Streamlit dashboard that turns the numbers into interactive maps, charts, and tables. You can see the biggest quakes of the day, explore which countries are most affected, or watch how magnitudes have changed over time.
What makes QuakeWatch special is that it runs automatically. I set up an ETL pipeline that updates every six hours so the dashboard and API are always up to date without me needing to manually trigger anything. That means it is not just a class demo, it is a small but complete data system that shows how real world pipelines are designed from extraction all the way to visualization.

---

## 📖 Project Overview

QuakeWatch is a real-time earthquake monitoring system that collects, processes, and visualizes global seismic activity.  
The goal is to provide a clean, structured dataset and a live dashboard for researchers, analysts, and the public to track earthquakes as they happen.

The pipeline runs automatically every **6 hours** to keep the data fresh.  
This project was designed to demonstrate a full ETL lifecycle, automation with cron, and modern visualization techniques.

## 🏗 Architecture (How It Works)

QuakeWatch is organized into three core layers:
ETL Pipeline (Extract, Transform, Load)
Extracts raw earthquake events from the USGS feed.
Transforms and validates the data using Pandas and Pandera.
Loads the events into a relational database (SQLite locally, PostgreSQL in deployment).
API (FastAPI)
Serves clean earthquake data directly from the database.
Provides endpoints for recent events, country-level statistics, and health checks.
Includes interactive documentation via Swagger UI at /docs.
Dashboard (Streamlit)
Interactive web application for exploring seismic activity.
Features include:
Recent earthquake tables with filtering.
Magnitude distribution over time.
A map view for global visualization.
Adjustable filters for minimum magnitude and number of rows.
Together, these parts form a complete pipeline: raw data goes in, structured insights come out, and both developers and non-technical users can explore earthquakes in ways that would otherwise require digging through complex JSON feeds.

---
## 🔧 How I Built It

- **Extraction** – Python script retrieves raw earthquake data from the USGS API.  
- **Transformation** – Data is cleaned, enriched (e.g., extracting country info), validated with [Pandera](https://pandera.readthedocs.io/), and structured for analytics.  
- **Loading** – Transformed events are stored in a SQL database.  
- **API Layer** – [FastAPI](https://fastapi.tiangolo.com/) service exposes REST endpoints.  
- **Dashboard** – [Streamlit](https://streamlit.io/) visualizes live earthquake data with maps, charts, and filters.  
- **Automation** – The ETL runs every 6 hours via a scheduled cron job.  

## 🎯 Purpose and Use Cases
QuakeWatch is useful for:
- 🧑‍🔬 Researchers studying seismic trends over time.  
- 🏛️ Governments & disaster-response teams monitoring earthquake activity.  
- 🎓 Educators and students learning about seismology and data pipelines.  
- 🌍 Anyone curious about real-time global earthquake activity.  

---

## 📌 System Overview

1. **ETL Pipeline**
   - **Extract**: Pulls earthquake data from the USGS API  
   - **Transform**: Cleans and structures the data (adds country/region, fixes types)  
   - **Load**: Stores processed events into a database  

2. **API (FastAPI)**
   - Serves structured earthquake data  
   - Endpoints for:
     - Recent earthquake events
     - Stats by country
     - Health checks
   - Fully documented with Swagger UI at `/docs`  

3. **Dashboard (Streamlit)**
   - Interactive dashboard with:
     - Country-by-country counts
     - Recent events table
     - Magnitude timeline
     - World map of events
   - Adjustable filters  


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

├── app/                # API & Dashboard code

│   ├── api.py          # FastAPI service

│   ├── dashboard.py    # Streamlit dashboard

│   ├── db.py           # Database connection

│   └── models.py       # ORM models

│
├── etl/                # ETL pipeline

│   ├── extract.py      # Fetch earthquake data

│   ├── transform.py    # Clean & validate

│   ├── load.py         # Load into DB

│   └── flow.py         # Orchestrated ETL

│
├── templates/          # HTML templates

│   └── events.html

│
├── tests/              # Unit tests

│   ├── test_api.py

│   └── test_transform.py

│
├── requirements.txt    # Python dependencies

├── docker-compose.yml  # Optional multi-service setup

├── Makefile            # Automation commands

├── local.db            # SQLite database

├── etl_cron.log        # Logs from scheduled runs

└── README.md           # Documentation

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
