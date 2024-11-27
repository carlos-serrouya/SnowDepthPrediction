import os
import csv
import pandas as pd
import numpy as np

def getENSOData():
    """
    Mock function for ENSO (El Nino/La Nina) data retrieval.
    Currently assumes data is stored in CSV files.
    """
    carbon_data = {}
    elnino_data = {}
    lanina_data = {}

    with open("carbon.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            carbon_data[row[0]] = row[1]

    with open("elnino.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            elnino_data[row[0]] = row[1]

    with open("lanina.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            lanina_data[row[0]] = row[1]

    return elnino_data, lanina_data, carbon_data

def complete_seasons(data):
    """
    Identifies viable seasons with complete or near-complete data.
    """
    viable_seasons = []
    season_start_date = "06-01"  # Define season start as June 1st

    summer = ["06", "07", "08"]
    winter = ["10", "11", "12", "01", "02", "03", "04"]

    # Create a season key for each entry
    data["SEASON_YEAR"] = np.where(
        data["MONTH"].isin(summer),
        data["YEAR"],
        data["YEAR"] - (data["MONTH"].isin(winter).astype(int))
    )
    grouped = data.groupby("SEASON_YEAR")

    for season, group in grouped:
        if len(group) >= 355:  # A threshold for "complete" season
            viable_seasons.append(season)

    return viable_seasons

def processCSV(csv_file):
    """
    Processes a single climate data CSV to aggregate seasonal data.
    """
    # Load data
    data = pd.read_csv(csv_file, parse_dates=["LOCAL_DATE"])
    data["DATE"] = pd.to_datetime(data["LOCAL_DATE"])
    data["YEAR"] = data["DATE"].dt.year
    data["MONTH"] = data["DATE"].dt.month

    summer = [6, 7, 8]
    winter = [10, 11, 12, 1, 2, 3, 4]

    # Find viable seasons
    viable_seasons = complete_seasons(data)

    yearly_snow = []
    summer_temp = []
    averages = []

    # Aggregate seasonal data
    for season in viable_seasons:
        season_data = data[data["SEASON_YEAR"] == season]

        # Summer stats
        summer_data = season_data[season_data["MONTH"].isin(summer)]
        avg_summer_temp = summer_data["MAX_TEMPERATURE"].mean()

        # Winter stats
        winter_data = season_data[season_data["MONTH"].isin(winter)]
        total_winter_snow = winter_data["TOTAL_SNOW"].sum()

        yearly_snow.append(total_winter_snow)
        summer_temp.append(avg_summer_temp)
        averages.append((total_winter_snow + yearly_snow[-1]) / 2 if len(yearly_snow) > 1 else total_winter_snow)

    return yearly_snow, summer_temp, averages

def process_folder(path):
    """
    Processes all CSV files in a directory to extract seasonal data.
    """
    X = []
    Y = []
    files = os.listdir(path)

    for file in files:
        if file.endswith(".csv"):
            x, y = processCSV(os.path.join(path, file))
            X.append(x)
            Y.append(y)

    return X, Y
