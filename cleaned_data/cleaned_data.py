import pandas as pd
import os

# File paths
csv_file1 = '/mnt/c/Users/ASUS/Documents/research2/Prediction-Popular-Song/data/data_with_audio.csv'
csv_file2 = '/mnt/c/Users/ASUS/Documents/research2/Prediction-Popular-Song/data_not_found/emptynotmatch.csv'

# Load the first CSV file
df1 = pd.read_csv(csv_file1)

# Check if second file exists and is readable
if os.path.exists(csv_file2):
    try:
        df2 = pd.read_csv(csv_file2, encoding='utf-8', on_bad_lines='skip')
        
        if df2.empty:
            print("Warning: emptynotmatch.csv is empty.")
            df2 = pd.DataFrame(columns=['uri'])  # Create empty DataFrame if needed

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty or unreadable.")
        df2 = pd.DataFrame(columns=['uri'])  # Prevent errors

else:
    print(f"Error: File '{csv_file2}' not found.")
    df2 = pd.DataFrame(columns=['uri'])  # Prevent errors

# Ensure 'uri' column exists
if 'uri' in df1.columns and 'uri' in df2.columns:
    df1_filtered = df1[~df1['uri'].isin(df2['uri'])]  # Remove matching URIs
    json_data1_filtered = df1_filtered.to_json(orient='records')
    print(json_data1_filtered)  # Output cleaned JSON
else:
    print("Error: 'uri' column not found in one of the CSV files.")

# Save the cleaned data to a new CSV file
df1_filtered.to_csv('/mnt/c/Users/ASUS/Documents/research2/Prediction-Popular-Song/cleaned_data/cleaned_data_filtered.csv', index=False)