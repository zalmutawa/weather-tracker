#import statements - these are the libraries we need to use in our code
import csv
import os
import re
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

#Zahras Components
def recordObservation():
    file_exists = os.path.isfile("observations.csv")
    file_empty = os.path.getsize("observations.csv") == 0 if file_exists else True

    #read existing dates
    existing_dates = set()
    if file_exists and not file_empty:
        with open("observations.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                existing_dates.add(row[0])

    # date
    while True:
        date = input("Enter date (MM-DD-YYYY): ")
        
        try:
            date_obj = datetime.strptime(date, "%m-%d-%Y")
            min_date = datetime(2025, 1, 1)
            today = datetime.today()
            
            if date_obj < min_date:
                print("**Date must be from 2025 onwards**")
            elif date_obj > today:
                print("**Date cannot be in the future**")
            elif date in existing_dates:
                print("**This date already exists**")
            else:
                break
                
        except:
            print("**Invalid format.. use MM-DD-YYYY**")

    # temp
    while True:
        temp = input("Enter temperature (C): ")
        try:
            temp_value = float(temp)
            if temp_value < -50 or temp_value > 60:
                print("**temperature must not exceed two digits**")
                continue
            break
        except:
            print("**Temperature must be a number**")

    # condition
    while True:
        cond = input("Enter condition (Sunny, Cloudy, Rainy or Windy): ")
        
        valid_conditions = ["sunny", "cloudy", "rainy", "windy"]
        if cond.lower() in valid_conditions:
            cond = cond.capitalize()
            break
        print("**Condition must be a word (e.g., sunny, rainy)**")

    # humidity
    while True:
        humidity = input("Enter humidity (%): ")
        if humidity.isdigit():
            h_value = int(humidity)
            if 0 <= h_value <= 100:
                break
            else:
                print("**Humidity must be between 0 and 100**")
        else:
            print("**Humidity must be a whole number**")

    # wind speed
    while True:
        wind_speed = input("Enter wind speed (km/h): ")
        try:
            w_value = float(wind_speed)
            if w_value < 0:
                print("**Wind speed cannot be negative**")
            elif w_value > 200:
                print("**Wind speed is unrealistically high**")
            else:
                break
        except:
            print("**Wind speed must be a number**")

    new_row = [date, temp_value, cond, h_value, w_value]

    with open("observations.csv", mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists or file_empty:
            writer.writerow(["Date", "Temperature", "Condition", "Humidity", "Wind Speed"])

        writer.writerow(new_row)

    print("-Your observation is recorded-")
    
def search():
    search_date = input("Enter the date (MM-DD-YYYY): ")
    
    if not re.match(r"\d\d-\d\d-\d\d\d\d", search_date):
        print("Invalid date format .. enter MM-DD-YYYY")
        return

    if not os.path.isfile("observations.csv"):
        print("data file not found")
        return

    date_found = False

    with open("observations.csv", mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            if row[0] == search_date:
                if not date_found:
                    print("\nResults:\n")
                    print(", ".join(header))
                print(", ".join(row))
                date_found = True

    if not date_found:
        print("There are no observations for this date")

def displayTrends():
    if not os.path.isfile("observations.csv") or os.path.getsize("observations.csv") == 0:
        print("No data available")
        return

    observations = []
    with open("observations.csv", mode="r") as file:
        reader = csv.reader(file)
        try:
            header = next(reader)
        except StopIteration:
            print("File is empty.")
            return
        
        for row in reader:
            if not row or len(row) < 2:
                continue
                
            try:
                row_date = datetime.strptime(row[0], "%m-%d-%Y")
                temp_value = float(row[1])
                observations.append([row_date, row[0], temp_value])
            except ValueError:
                continue

    if not observations:
        print("No valid data to display.")
        return

    observations.sort(key=lambda x: x[0], reverse=True)
    print("\n--- Temperature Trends ---")
    print(f"{'Date':<12} | {'Trend'}")
    print("-" * 35)

    for obs in observations:
        date_str = obs[1]
        temp = obs[2]
        num_bars = max(1, int(abs(temp) // 2))
        bar = "|" * num_bars
        
        print(f"{date_str:<12} | {bar} {temp}°C")
                    

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

    
def load_observations():
    """
    Read all rows from the CSV file and return them as a list of dicts.
    """
    observations = []
    with open(CSV_FILE, mode="r", newline="\n") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Cast numeric columns so math works later
            row["temperature_c"]   = float(row["temperature_c"])
            row["humidity_pct"]    = float(row["humidity_pct"])
            row["wind_speed_kmh"]  = float(row["wind_speed_kmh"])
            observations.append(row)
    return observations
    
def view_all_observations():
    """
    Display all recorded observations in a formatted table.
    """
    observations = load_observations()
    if not observations:
        print("\nNo observations recorded yet.")
        return
    try:
        from tabulate import tabulate
        print(tabulate(observations, headers="keys", tablefmt="fancy_grid"))
    except ImportError:
        headers = list(observations[0].keys())
        print("  ".join(f"{h:<18}" for h in headers))
        print("-" * 80)
        for obs in observations:
            print("  ".join(f"{str(obs[h]):<18}" for h in headers))


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

def compare_years(observations):
    """
    Compare average, min, and max temperature across different years.
    """
    if not observations:
        print("\nNo observations recorded yet.")
        return

    current_year = datetime.today().year
    by_year = {}
    for obs in observations:
        year = int(obs["date"].split("-")[2])
        by_year.setdefault(year, []).append(obs)

    if len(by_year) < 2:
        print("\nNot enough data to compare years (need at least 2 different years).")
        return

    print("\n--- Year-by-Year Comparison ---")
    for year in sorted(by_year):
        temps = [o["temperature_c"] for o in by_year[year]]
        avg = round(statistics.mean(temps), 1)
        label = " (current)" if year == current_year else ""
        print(f"  {year}{label}: {len(by_year[year])} obs | avg {avg}°C | min {min(temps)}°C | max {max(temps)}°C")


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

#Hadi's Components 

def check_record():
    observations = load_observations()

    if not observations:
        print("\nNo observations recorded yet.")
        return

    threshold = 20.0
    hottest = max(observations, key=lambda obs: obs["temperature_c"])

    if hottest["temperature_c"] > threshold:
        print("\n=== Record-Breaking Temperature ===")
        print(f"  Date        : {hottest['date']}")
        print(f"  Temperature : {hottest['temperature_c']}°C  *** NEW RECORD ***")
        print(f"  Condition   : {hottest['condition']}")
        print(f"  Humidity    : {hottest['humidity_pct']}%")
        print(f"  Wind Speed  : {hottest['wind_speed_kmh']} km/h")
    else:
        print(f"\nNo observation exceeded the threshold of {threshold}°C.")

    return hottest


def display_menu():
    """Display the main menu options."""
    print("\n=== Weather Tracker ===")
    print("1. Record a new observation")
    print("2. View weather statistics")
    print("3. Search observations by date")
    print("4. View all observations")
    print("--- Stretch Goals ---")
    print("5. Display temperature trends")
    print("6. Filter by month")
    print("7. Filter by season")
    print("8. Predict tomorrow's weather")
    print("9. Compare current year with previous years")
    print("10. Check record-breaking temperatures")
    print("11. Exit")
    return input("Enter your choice (1-11): ")


def main():
    """Main application loop."""
    init_csv()
    print("Welcome to Weather Tracker!")

    while True:
        choice = display_menu()

        if choice == '1':
            recordObservation()
        elif choice == '2':
            observations = load_observations()
            view_statistics(observations)
        elif choice == '3':
            search()
        elif choice == '4':
            view_all_observations()
        elif choice == '5':
            displayTrends()
        elif choice == '6':
            observations = load_observations()
            try:
                month = int(input("Enter month number (1-12): "))
                results = filter_by_month(observations, month)
                print(f"\nFound {len(results)} observation(s).")
                view_statistics(results)
            except ValueError:
                print("Invalid month. Please enter a number between 1 and 12.")
        elif choice == '7':
            observations = load_observations()
            season = input("Enter season (Winter, Spring, Summer, Fall): ")
            results = filter_by_season(observations, season)
            print(f"\nFound {len(results)} observation(s).")
            view_statistics(results)
        elif choice == '8':
            observations = load_observations()
            predict_tomorrow(observations)
        elif choice == '9':
            observations = load_observations()
            compare_years(observations)
        elif choice == '10':
            check_record()
        elif choice == '11':
            print("Thank you for using Weather Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 11.")
        