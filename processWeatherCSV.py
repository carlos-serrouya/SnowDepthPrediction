LONGITUDE = 0
LATITUDE = 1
AVG_SUMMER_MAX = 2
AVG_SUMMER_LOW = 3
TOTAL_SUMMER_RAIN = 4
AVERAGE_PREVIOUS_SNOWFALL = 5
LANINA_DATA = 6
ELNINO_DATA = 7
LANINAINTENSITY_DATA = 8
ELNINOINTENSITY_DATA = 9
CARBON_DATA = 10
ELEVATION = 11
SEASON = 12
YEARLY_SNOW = 13

import os
import csv
import pandas as pd
import numpy as np
import requests
from getLaCar import process_file, la_main

global_dic = la_main()

def getElevation(longitude, latitude):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={latitude},{longitude}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        result = response.json()["results"][0]
        result = int(result["elevation"])
        print(f"Elevation for {latitude}, {longitude}: {result} meters")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error fetching elevation data: {e}")
        return None
    #return 0


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
            if season > 1950:
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

    longitude = data["x"][5]
    latitude = data["y"][5]

    elevation = getElevation(longitude, latitude)
    if elevation is None:
        return False, []

    # Define summer and winter months
    summer = [6, 7, 8]
    winter = [10, 11, 12, 1, 2, 3, 4]

    # Find viable seasons
    viable_seasons = complete_seasons(data)

    location_data = []

    # Initialize a list to store total snow for each season
    previous_season_snowfall = []

    print(viable_seasons)
    # Aggregate seasonal data
    for season in viable_seasons:
        # Skip the first season because it has no prior data for the average
        if season == viable_seasons[0] or global_dic[season][4] == 0:
            continue

        # Filter winter data (Oct-Dec current year + Jan-Apr next year)
        oct_dec_data = data[(data["YEAR"] == season) & (data["MONTH"].isin([10, 11, 12]))]
        jan_apr_data = data[(data["YEAR"] == season + 1) & (data["MONTH"].isin([1, 2, 3, 4]))]
        winter_data = pd.concat([oct_dec_data, jan_apr_data])

        # Calculate total snow for the current winter season
        this_season_snow = winter_data["TOTAL_SNOW"].sum()

        # Filter summer data (June-August of the current season year)
        summer_data = data[(data["YEAR"] == season) & (data["MONTH"].isin(summer))]

        # Calculate summer stats
        avg_summer_max = summer_data["MAX_TEMPERATURE"].mean()
        total_summer_rain = summer_data["TOTAL_RAIN"].sum()
        avg_summer_low = summer_data["MIN_TEMPERATURE"].mean()

        # Calculate the average snowfall from all prior seasons
        if previous_season_snowfall:
            average_previous_snowfall = sum(previous_season_snowfall) / len(previous_season_snowfall)
        else:
            oct_dec_data = data[(data["YEAR"] == season-1) & (data["MONTH"].isin([10, 11, 12]))]
            jan_apr_data = data[(data["YEAR"] == season) & (data["MONTH"].isin([1, 2, 3, 4]))]
            winter_data = pd.concat([oct_dec_data, jan_apr_data])

            # Calculate total snow for the current winter season
            last_season_snowfall = winter_data["TOTAL_SNOW"].sum()
            average_previous_snowfall = last_season_snowfall

        
        # Get ENSO and carbon data for the current season
        dic_data = global_dic[season]
         # 0 is lanina, 1 is elnino, 2 is lanina intensity, 3 is elnino intensity, 4 is deseasonalized carbon
        lanina_data = dic_data[0]
        elnino_data = dic_data[1]
        laninaintensity_data = dic_data[2]
        elninointensity_data = dic_data[3]
        carbon_data = dic_data[4]

        if this_season_snow == 0 or total_summer_rain == 0:
            continue
        # Store the results for this season
        location_data.append([longitude, latitude, avg_summer_max, avg_summer_low, total_summer_rain, average_previous_snowfall, lanina_data, elnino_data, laninaintensity_data, elninointensity_data, carbon_data, elevation, season, this_season_snow])


        # Update the list of previous season snowfall
        previous_season_snowfall.append(this_season_snow)

    #remove first row from location_data
    
    if len(location_data) > 5:
        location_data.pop(0)
        #normalize data minus longitude and latitude, elevation, and season
        location_data = np.array(location_data)
        
        return True, location_data
    else:
        return False, location_data


def process_folder(path):
    """
    Processes all CSV files in a directory to extract seasonal data.
    """
    saving_data = []
    path = os.path.join(os.getcwd(), path)
    files = os.listdir(path)

    for file in files:
        if file.endswith(".csv"):
            worked, location_data = processCSV(os.path.join(path, file))
            if worked:
                saving_data.extend(location_data)

    return saving_data


def main():
    """
    Main function to demonstrate the processCSV function.
    """
    ElNino_file_path = "ElNinoLaNina.csv"
    Carbon_file_path = "carbon_data.csv"
    # Process ENSO and carbon data
    folder_path = "csv_folder"
    import os
    working_directory = os.getcwd()
    folder_path = os.path.join(working_directory, folder_path)

    data = process_folder(folder_path)
    for i, row in enumerate(data):
        try:
            np.array(row)
        except:
            print(row)
    np.array(data)
    save_loc = "processed_data"

    np.save(save_loc, data)

main()