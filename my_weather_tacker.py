#import statements - these are the libraries we need to use in our code
import csv
import os
import statistics
from datetime import datetime
from collections import Counter

# Constants 
CSV_FILE = "observations.csv"
CSV_HEADERS = ["date", "temperature_c", "condition", "humidity_pct", "wind_speed_kmh"]

VALID_CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy"]

SEASON_MAP = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Fall",   10: "Fall",  11: "Fall",
}

# Zainabs Components      
def init_csv():
    """
    Check if the observations CSV file exists.
    If not, create it and write the header row.
    """
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="\n") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        print(f"Just created a new csv file: {CSV_FILE}")
    else:
        print(f"Loaded existing csv file: {CSV_FILE}")

    
def load_observations(self):
    """
    Read all rows from the CSV file and return them as a list of dicts.
    """
    observations = []
    if not os.path.exists(CSV_FILE):
        return observations  # Return empty list if file doesn't exist
    
    with open(CSV_FILE, mode="r", newline="\n") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Cast numeric columns so math works later
            row["temperature_c"] = float(row["temperature_c"])
            row["humidity_pct"] = float(row["humidity_pct"])
            row["wind_speed_kmh"] = float(row["wind_speed_kmh"])
            observations.append(row)
    
    return observations
    
def view_statistics(observations):
    """
    Compute and display summary statistics from all recorded observations.

    Stats shown:
        - Average, min, and max temperature
        - Most commonly recorded weather condition

    """
    if not observations:
        print("\n No observations recorded yet.")
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
    
def filter_by_month(observations, month):
    """
    Filter observations to only include a specific month.
    """
    results = []

    for obs in observations:
        # Step 1: pull the date string out and convert it to a datetime object
        date_object = datetime.strptime(obs["date"], "%m-%d-%Y")

        # Step 2: extract just the month number from it
        obs_month = date_object.month

        # Step 3: check if it matches, and add to results if so
        if obs_month == month:
            results.append(obs)

    return results


def filter_by_season(observations, season):
    """
    Filter observations to only include a specific season.
    """
    
    matching_observations = []

    for obs in observations:
        date_string = obs["date"]
        month = int(date_string.split("-")[0])

        if month == 12 or month == 1 or month == 2:
            obs_season = "Winter"
        elif month == 3 or month == 4 or month == 5:
            obs_season = "Spring"
        elif month == 6 or month == 7 or month == 8:
            obs_season = "Summer"
        else:
            obs_season = "Fall"

        if obs_season == season.capitalize():
            matching_observations.append(obs)

    return matching_observations

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_tomorrow(observations):
    if not observations:
        print("No observations recorded yet.")
        return

    # --- Step 1: Prepare the data ---
    months = []
    temperatures = []
    conditions = []

    for obs in observations:
        month = int(obs["date"].split("-")[0])
        months.append(month)
        temperatures.append(obs["temperature_c"])
        conditions.append(obs["condition"])

    # sklearn needs a 2D array for input, so we reshape
    # [[1], [2], [3]] instead of [1, 2, 3]
    months_2d = [[m] for m in months]

    # --- Step 2: Predict temperature (a number) ---
    temp_model = LinearRegression()
    temp_model.fit(months_2d, temperatures)

    current_month = datetime.today().month
    predicted_temp = temp_model.predict([[current_month]])
    predicted_temp = round(predicted_temp[0], 1)

    # --- Step 3: Predict condition (a category like "Sunny", "Rainy") ---
    condition_model = KNeighborsClassifier(n_neighbors=3)
    condition_model.fit(months_2d, conditions)

    predicted_condition = condition_model.predict([[current_month]])
    predicted_condition = predicted_condition[0]

    # --- Step 4: Print results ---
    current_month_name = datetime.today().strftime("%B")

    print("Tomorrow's Prediction (based on historical data)")
    print("Month: " + current_month_name)
    print("Predicted temperature: " + str(predicted_temp) + "C")
    print("Likely condition: " + str(predicted_condition))
    print("This is an estimate based on a real forecast.")    