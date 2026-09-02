# 🌱 School Green Campus Sustainability Dashboard

A Streamlit web application for tracking school-campus sustainability activities.

## Features
- User/date based data entry
- Energy and water tracking
- Total, recycled and green waste tracking
- Trees and plants/saplings tracking
- Rainwater harvesting and solar energy tracking
- Dashboard metrics and charts
- User/class filters
- CSV download
- **Green Guardians** leaderboard
- Eco-friendly tips
- Green sidebar and clean interface

## Files
- `app.py` — main application
- `requirements.txt` — required packages
- `green_campus_data.csv` — data storage file

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub + Streamlit
Upload `app.py`, `requirements.txt`, `README.md`, `.gitignore`, `.streamlit/config.toml`,
and `green_campus_data.csv` to your GitHub repository.

Then deploy the repository using Streamlit Community Cloud and select `app.py`
as the main file.

## Important
CSV storage is suitable for a school-project prototype. For a real public
multi-user application, use a database such as PostgreSQL/Supabase/Firebase
to avoid simultaneous-write problems.

## Flow
**Enter Details → Submit → Dashboard → Tracking / Green Guardians / Eco Tips**

## Green Guardians scoring
- Tree planted = 10 points
- Plant/sapling = 3 points
- Recycled waste = 2 points per kg
- Green waste = 1 point per kg
- Rainwater harvested = 1 point per 100 L
- Solar energy = 0.5 point per kWh

Badges:
- 0–49: Eco Explorer
- 50–149: Green Starter
- 150–299: Eco Warrior
- 300–499: Green Guardian
- 500+: Earth Champion
