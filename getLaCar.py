import pandas as pd

def process_file(carbon_file_path, elnino_file_path):
    # Initialize the dictionary to store deseasonalized dics by year
    dic = {}
    # add every year from 1948-2024 to the dictionary
    for i in range(1948, 2025):
        # 0 is lanina, 1 is elnino, 2 is lanina intensity, 3 is elnino intensity, 4 is deseasonalized carbon
        dic[i] = [0,0,0,0,0]

    with open(carbon_file_path, 'r') as file:
        # Skip the header line
        next(file)
        next(file)
        
        # Read each line in the file
        for line in file:
            # Split the line by tabs (or spaces) to extract columns
            columns = line.split()
            
            # Extract relevant data: year, month, and deseasonalized dic
            year = int(columns[0])  # Year is in the first column
            month = int(columns[1])  # Month is in the second column
            deseasonalized_avg = float(columns[4])  # Deseasonalized dic is in the eighth column
            
            # Only process lines where the month is 8 (August)
            if month == 8:
                # Add the deseasonalized dic to the dictionary for that year
                dic[year][4] = deseasonalized_avg

    # Read the ENSO data
    df = pd.read_csv(elnino_file_path)
    for _, row in df.iterrows():
        year = row['Year']
        classification = row['el/la']
        intensity = row['intensity']
        
        if classification == 'la':
            dic[year][0] = 1
            dic[year][2] = intensity
        else:
            dic[year][1] = 1
            dic[year][3] = intensity


    return dic

def la_main():
    # Path to the text file (adjust the path as necessary)
    carbon_file_path = 'carbon_data.txt'

    el_nino_file_path = 'ElNinoLaNina2.csv'

    # Call the function to process the file
    dic = process_file(carbon_file_path, el_nino_file_path)

    # Output the dictionary of deseasonalized dics by year
    print(dic)
    return dic
la_main()