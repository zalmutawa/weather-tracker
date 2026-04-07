"""
weather_utils.py
----------------
Utility functions for the Weather Tracker application.
All data is stored in and read from 'observations.csv'.

CSV columns: date, temperature_c, condition, humidity_pct, wind_speed_kmh
"""

import csv
import os
import statistics
from datetime import datetime
from collections import Counter

# ── Constants ────────────────────────────────────────────────────────────────

CSV_FILE = "observations.csv"
CSV_HEADERS = ["date", "temperature_c", "condition", "humidity_pct", "wind_speed_kmh"]

VALID_CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy"]

SEASON_MAP = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Fall",   10: "Fall",  11: "Fall",
}


# ── CSV Setup & Loading ───────────────────────────────────────────────────────

def init_csv():
    """
    Check if the observations CSV file exists.
    If not, create it and write the header row.
    Called once at app startup.
    """
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        print(f"📁 Created new file: {CSV_FILE}")
    else:
        print(f"📂 Loaded existing file: {CSV_FILE}")


def load_observations():
    """
    Read all rows from the CSV file and return them as a list of dicts.
    Each dict has keys matching CSV_HEADERS.
    Numeric fields are cast to float for calculations.

    Returns:
        list[dict]: All recorded observations, or [] if file is empty.
    """
    observations = []
    with open(CSV_FILE, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Cast numeric columns so math works later
            row["temperature_c"]   = float(row["temperature_c"])
            row["humidity_pct"]    = float(row["humidity_pct"])
            row["wind_speed_kmh"]  = float(row["wind_speed_kmh"])
            observations.append(row)
    return observations


# ── Input Validation Helpers ─────────────────────────────────────────────────

def validate_date(date_str):
    """
    Check that a string matches the MM-DD-YYYY format.

    Args:
        date_str (str): The date string entered by the user.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%m-%d-%Y")
        return True
    except ValueError:
        return False


def validate_number(value_str):
    """
    Check that a string can be converted to a float.

    Args:
        value_str (str): The input string to test.

    Returns:
        bool: True if numeric, False otherwise.
    """
    try:
        float(value_str)
        return True
    except ValueError:
        return False


def validate_condition(condition_str):
    """
    Check that the given condition is in the list of allowed values.
    Case-insensitive — 'sunny' and 'Sunny' both pass.

    Args:
        condition_str (str): The condition entered by the user.

    Returns:
        bool: True if valid, False otherwise.
    """
    return condition_str.strip().capitalize() in VALID_CONDITIONS


def get_valid_input(prompt, validator, error_msg):
    """
    Repeatedly prompt the user until their input passes a validator.
    Keeps the input loop out of the main feature functions.

    Args:
        prompt (str):      The message shown to the user.
        validator (func):  A function that takes a string and returns bool.
        error_msg (str):   Message shown when validation fails.

    Returns:
        str: The validated input string.
    """
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f"  ⚠️  {error_msg}")


# ── Core Features ─────────────────────────────────────────────────────────────

def display_menu():
    """
    Print the main menu and return the user's choice as a string.
    Does not handle any logic — just displays options and reads input.

    Returns:
        str: The option number entered by the user (e.g. '1', '2', ...).
    """
    print("\n" + "=" * 40)
    print("       🌤️  Weather Tracker")
    print("=" * 40)
    print("  1. Record a new observation")
    print("  2. View weather statistics")
    print("  3. Search observations by date")
    print("  4. View all observations")
    print("  5. Exit")
    print("=" * 40)
    return input("Enter your choice (1-5): ").strip()


def record_observation():
    """
    Prompt the user for all weather fields, validate each input,
    and append the new observation as a row in the CSV file.

    Fields collected:
        - date          : MM-DD-YYYY
        - temperature_c : float (degrees Celsius)
        - condition     : one of VALID_CONDITIONS
        - humidity_pct  : float (0–100)
        - wind_speed_kmh: float (>= 0)
    """
    print("\n--- Record New Observation ---")

    date = get_valid_input(
        "Date (MM-DD-YYYY): ",
        validate_date,
        "Invalid date format. Please use MM-DD-YYYY (e.g. 04-07-2026)."
    )

    temp = get_valid_input(
        "Temperature (°C): ",
        validate_number,
        "Please enter a valid number (e.g. 23.5)."
    )

    print(f"Conditions: {', '.join(VALID_CONDITIONS)}")
    condition = get_valid_input(
        "Condition: ",
        validate_condition,
        f"Please choose from: {', '.join(VALID_CONDITIONS)}."
    ).capitalize()

    humidity = get_valid_input(
        "Humidity (%): ",
        validate_number,
        "Please enter a number between 0 and 100."
    )

    wind = get_valid_input(
        "Wind speed (km/h): ",
        validate_number,
        "Please enter a valid number (e.g. 15.0)."
    )

    # Write the new row to the CSV
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, float(temp), condition, float(humidity), float(wind)])

    print(f"\n✅ Observation for {date} saved successfully!")


def view_statistics(observations):
    """
    Compute and display summary statistics from all recorded observations.

    Stats shown:
        - Average, min, and max temperature
        - Most commonly recorded weather condition

    Args:
        observations (list[dict]): The loaded observations list.
    """
    if not observations:
        print("\n⚠️  No observations recorded yet.")
        return

    temps = [obs["temperature_c"] for obs in observations]
    conditions = [obs["condition"] for obs in observations]

    avg_temp  = round(statistics.mean(temps), 1)
    min_temp  = min(temps)
    max_temp  = max(temps)
    top_cond  = Counter(conditions).most_common(1)[0][0]

    print("\n--- Weather Statistics ---")
    print(f"  Total observations : {len(observations)}")
    print(f"  Average temperature: {avg_temp}°C")
    print(f"  Min temperature    : {min_temp}°C")
    print(f"  Max temperature    : {max_temp}°C")
    print(f"  Most common cond.  : {top_cond}")


def search_by_date(observations):
    """
    Prompt the user for a date and display all matching observations.

    Args:
        observations (list[dict]): The loaded observations list.
    """
    if not observations:
        print("\n⚠️  No observations recorded yet.")
        return

    date = get_valid_input(
        "\nEnter date to search (MM-DD-YYYY): ",
        validate_date,
        "Invalid format. Use MM-DD-YYYY."
    )

    results = [obs for obs in observations if obs["date"] == date]

    if not results:
        print(f"\n  No observations found for {date}.")
        return

    print(f"\n--- Results for {date} ---")
    for obs in results:
        print(
            f"  🌡  {obs['temperature_c']}°C  |  {obs['condition']}  |  "
            f"💧 {obs['humidity_pct']}%  |  💨 {obs['wind_speed_kmh']} km/h"
        )


def view_all_observations(observations):
    """
    Display all recorded observations as a formatted table.
    Columns are padded with f-strings for alignment.

    Args:
        observations (list[dict]): The loaded observations list.
    """
    if not observations:
        print("\n⚠️  No observations recorded yet.")
        return

    # Table header
    print("\n" + "-" * 62)
    print(f"  {'Date':<12} {'Temp(°C)':<10} {'Condition':<10} {'Humidity':<10} {'Wind km/h'}")
    print("-" * 62)

    for obs in observations:
        print(
            f"  {obs['date']:<12} "
            f"{obs['temperature_c']:<10} "
            f"{obs['condition']:<10} "
            f"{obs['humidity_pct']:<10} "
            f"{obs['wind_speed_kmh']}"
        )

    print("-" * 62)
    print(f"  Total: {len(observations)} observation(s)")


# ── Stretch Goals ─────────────────────────────────────────────────────────────

def display_temperature_trend(observations):
    """
    Print a simple ASCII bar chart of temperature over time.
    Each row shows a date and a bar scaled to its temperature value.
    Negative temperatures are handled with a separate left bar.

    Args:
        observations (list[dict]): The loaded observations list.
    """
    if not observations:
        print("\n⚠️  No observations recorded yet.")
        return

    print("\n--- Temperature Trend ---")
    max_temp = max(obs["temperature_c"] for obs in observations)
    max_bar  = 30  # max number of characters in the bar

    for obs in observations:
        temp = obs["temperature_c"]
        # Scale bar length relative to the max temperature
        bar_len = int((temp / max_temp) * max_bar) if max_temp > 0 else 0
        bar = "█" * bar_len
        print(f"  {obs['date']}  {bar:<30}  {temp}°C")


def filter_by_month(observations, month):
    """
    Filter observations to only include a specific month.

    Args:
        observations (list[dict]): The loaded observations list.
        month (int): Month number (1–12).

    Returns:
        list[dict]: Observations matching the given month.
    """
    return [
        obs for obs in observations
        if datetime.strptime(obs["date"], "%m-%d-%Y").month == month
    ]


def filter_by_season(observations, season):
    """
    Filter observations by season name.
    Seasons: 'Winter' (Dec–Feb), 'Spring' (Mar–May),
             'Summer' (Jun–Aug), 'Fall' (Sep–Nov).

    Args:
        observations (list[dict]): The loaded observations list.
        season (str): One of 'Winter', 'Spring', 'Summer', 'Fall'.

    Returns:
        list[dict]: Observations from the given season.
    """
    return [
        obs for obs in observations
        if SEASON_MAP[datetime.strptime(obs["date"], "%m-%d-%Y").month] == season.capitalize()
    ]


def predict_tomorrow(observations):
    """
    Estimate tomorrow's weather based on historical data from the same month.
    Returns the most common condition and average temperature for that month
    across all years in the dataset.
    This is a statistical estimate, not a real forecast.

    Args:
        observations (list[dict]): The loaded observations list.
    """
    if not observations:
        print("\n⚠️  No observations recorded yet.")
        return

    current_month = datetime.today().month
    same_month_obs = filter_by_month(observations, current_month)

    if not same_month_obs:
        print(f"\n  Not enough historical data for month {current_month} yet.")
        return

    avg_temp   = round(statistics.mean(o["temperature_c"] for o in same_month_obs), 1)
    likely_cond = Counter(o["condition"] for o in same_month_obs).most_common(1)[0][0]

    print("\n--- Tomorrow's Prediction (based on historical data) ---")
    print(f"  📅 Month          : {datetime.today().strftime('%B')}")
    print(f"  🌡  Avg temperature: {avg_temp}°C")
    print(f"  ☁️   Likely condition: {likely_cond}")
    print("  ⚠️  This is an estimate based on past patterns, not a real forecast.")


def compare_year_over_year(observations):
    """
    Group observations by year and compare average temperature
    and most common condition across years.

    Args:
        observations (list[dict]): The loaded observations list.
    """
    if not observations:
        print("\n⚠️  No observations recorded yet.")
        return

    # Group observations by year
    by_year = {}
    for obs in observations:
        year = datetime.strptime(obs["date"], "%m-%d-%Y").year
        by_year.setdefault(year, []).append(obs)

    if len(by_year) < 2:
        print("\n  ⚠️  Need at least 2 years of data for a comparison.")

    print("\n--- Year-Over-Year Comparison ---")
    print(f"  {'Year':<8} {'Avg Temp':<12} {'Top Condition'}")
    print("  " + "-" * 36)

    for year in sorted(by_year):
        year_obs   = by_year[year]
        avg_temp   = round(statistics.mean(o["temperature_c"] for o in year_obs), 1)
        top_cond   = Counter(o["condition"] for o in year_obs).most_common(1)[0][0]
        print(f"  {year:<8} {avg_temp:<12} {top_cond}")


def display_outliers(observations):
    """
    Find and display record-breaking observations:
        - Hottest day
        - Coldest day
        - Highest wind speed
        - Highest humidity

    Args:
        observations (list[dict]): The loaded observations list.
    """
    if not observations:
        print("\n⚠️  No observations recorded yet.")
        return

    hottest  = max(observations, key=lambda o: o["temperature_c"])
    coldest  = min(observations, key=lambda o: o["temperature_c"])
    windiest = max(observations, key=lambda o: o["wind_speed_kmh"])
    humid    = max(observations, key=lambda o: o["humidity_pct"])

    print("\n--- Record-Breaking Observations 🏆 ---")
    print(f"  🔥 Hottest   : {hottest['temperature_c']}°C on {hottest['date']}")
    print(f"  🥶 Coldest   : {coldest['temperature_c']}°C on {coldest['date']}")
    print(f"  💨 Windiest  : {windiest['wind_speed_kmh']} km/h on {windiest['date']}")
    print(f"  💧 Most humid: {humid['humidity_pct']}% on {humid['date']}")