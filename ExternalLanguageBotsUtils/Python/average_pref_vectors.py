import os
import pandas as pd
import numpy as np

# Specify the input folder containing CSV files and the output CSV file path
input_folder = 'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\Logs\\Preference_vectors'      # Replace with your input folder path
output_csv = 'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\Logs\\Preference_vector_average.csv'  # Replace with your desired output CSV path

# ==============================
# Processing Section
# ==============================

def compute_average_vectors(input_folder, output_csv, include_filenames=False):
    """
    Computes the average vector for each CSV file in the input_folder and writes them to output_csv.
    
    Parameters:
    - input_folder (str): Path to the folder containing input CSV files.
    - output_csv (str): Path where the output CSV will be saved.
    - include_filenames (bool): Whether to include the original filenames in the output CSV.
    """
    # Check if input folder exists
    if not os.path.isdir(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        return

    # List all CSV files in the input folder
    csv_files = [file for file in os.listdir(input_folder) if file.lower().endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in the folder '{input_folder}'. Please check the folder path and contents.")
        return
    
    print(f"Found {len(csv_files)} CSV file(s) in '{input_folder}'. Starting processing...\n")

    average_vectors = []
    filenames = []

    for idx, filename in enumerate(csv_files, start=1):
        file_path = os.path.join(input_folder, filename)
        print(f"Processing file {idx}/{len(csv_files)}: '{filename}'")

        try:
            # Read the CSV file without headers
            df = pd.read_csv(file_path, header=None)
            print(f" - Successfully read '{filename}' with shape {df.shape}")

            # Validate the number of columns
            expected_columns = 129
            if df.shape[1] != expected_columns:
                print(f" - Skipping '{filename}': Expected {expected_columns} columns, found {df.shape[1]}")
                continue

            # Ensure all data is numeric
            if not np.issubdtype(df.dtypes.values[0], np.number):
                print(f" - Attempting to convert data in '{filename}' to numeric.")
                df = df.apply(pd.to_numeric, errors='coerce')
                if df.isnull().values.any():
                    print(f"   - Warning: Non-numeric data found in '{filename}'. Skipping this file.")
                    continue

            # Compute the average vector
            avg_vector = df.mean(axis=0).values
            average_vectors.append(avg_vector)
            filenames.append(filename)
            print(f" - Average vector computed for '{filename}'.\n")

        except Exception as e:
            print(f" - Error processing '{filename}': {e}\n")
            continue

    if not average_vectors:
        print("No average vectors were computed. Please ensure your CSV files are correctly formatted.")
        return

    # Prepare the DataFrame for output
    if include_filenames:
        # Create a list of lists where each sublist starts with the filename
        combined_data = [[fname] + list(avg_vec) for fname, avg_vec in zip(filenames, average_vectors)]
        column_names = ['Filename'] + [f'col{i}' for i in range(1, expected_columns + 1)]
    else:
        combined_data = average_vectors
        column_names = [f'col{i}' for i in range(1, expected_columns + 1)]
    
    output_df = pd.DataFrame(combined_data, columns=column_names)

    # Save to CSV
    try:
        output_df.to_csv(output_csv, index=False)
        print(f"\nAll average vectors have been saved to '{output_csv}'.")
    except Exception as e:
        print(f"Error saving the output CSV '{output_csv}': {e}")

# ==============================
# Execution Section
# ==============================

if __name__ == "__main__":
    # Configure whether to include filenames in the output CSV
    include_filenames = False  # Set to True if you want filenames in the output

    # Call the function with the specified parameters
    compute_average_vectors(input_folder, output_csv, include_filenames)
