import os
import pandas as pd

def combine_csv_files(input_folder, output_folder):
    """
    Combines CSV files in the input_folder that start with the same two letters and saves them to output_folder.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Get a list of all CSV files in the input folder
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    
    # Track processed prefixes to avoid duplicating work
    processed_prefixes = set()
    
    for file in csv_files:
        # Extract the prefix (first 2 letters) of the file
        prefix = file[:2]
        
        # Skip if we've already processed this prefix
        if prefix in processed_prefixes:
            continue
        
        # Find all files starting with the same prefix
        matching_files = [f for f in csv_files if f.startswith(prefix)]
        
        # Load and combine the matching files
        combined_data = pd.DataFrame()
        for match in matching_files:
            file_path = os.path.join(input_folder, match)
            data = pd.read_csv(file_path)
            combined_data = pd.concat([combined_data, data], ignore_index=True)
        
        # Save the combined data to the output folder
        if not combined_data.empty:
            output_file = os.path.join(output_folder, f"{prefix}_combined.csv")
            combined_data.to_csv(output_file, index=False)
            print(f"Saved combined file: {output_file}")
        
        # Mark this prefix as processed
        processed_prefixes.add(prefix)

# Example usage
input_folder = 'csv_folder_seperate'
output_folder = 'csv_folder_together'

combine_csv_files(input_folder, output_folder)
