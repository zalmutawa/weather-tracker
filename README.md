# Weather Tracker

A Python CLI application for logging and analyzing local weather observations, with data persisted in a CSV file.

---

## Problem Statement

Weather enthusiasts want a simple tool to record daily conditions and explore patterns over time — without relying on external APIs or databases.

---

## Project Structure

```
weather-tracker/
├── my_weather_tacker.py       # Core Python module (all functions)
├── weather_tracker.ipynb      # Main demo notebook
├── observations.csv           # Persisted weather data (auto-created)
└── notebooks/
    ├── filterObservations.ipynb   # Demo: filter by month / season
    ├── predictTemp.ipynb          # Demo: predict tomorrow's weather
    └── viewStatistics.ipynb       # Demo: summary statistics
```

---

## Features

### Core

| Feature | Description |
|---|---|
| Record observation | Log date, temperature (°C), condition, humidity (%), wind speed (km/h) |
| View statistics | Average, min, max temperature + most common condition |
| Search by date | Retrieve all observations for a given date |
| View all observations | Display full history in a formatted table |

### Stretch Goals

| Feature | Description |
|---|---|
| Filter by month/season | Narrow observations to a specific month or season (Winter / Spring / Summer / Fall) |
| Predict tomorrow's weather | Uses `LinearRegression` for temperature and `KNeighborsClassifier` for condition, trained on historical data |

---

## Data Format

Observations are stored in `observations.csv` with the following columns:

```
date, temperature_c, condition, humidity_pct, wind_speed_kmh
```

- Date format: `MM-DD-YYYY`
- Conditions: `Sunny`, `Cloudy`, `Rainy`, `Snowy`, `Windy`

---

## How to Run

1. Install dependencies:
   ```bash
   pip install scikit-learn numpy
   ```

2. Run the main notebook or import the module directly:
   ```python
   from my_weather_tacker import init_csv, load_observations, view_statistics
   ```

3. On first run, `init_csv()` creates `observations.csv` automatically. On subsequent runs, it loads existing data.

---

## Key Functions

| Function | Description |
|---|---|
| `init_csv()` | Creates the CSV file if it doesn't exist; loads it otherwise |
| `load_observations()` | Returns all rows as a list of dicts with numeric fields cast |
| `view_statistics(observations)` | Prints summary stats (avg/min/max temp, most common condition) |
| `filter_by_month(observations, month)` | Returns observations for a given month number (1–12) |
| `filter_by_season(observations, season)` | Returns observations for a given season string |
| `predict_tomorrow(observations)` | Predicts next day's temperature and condition using ML |
