import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_vector_index_from_single_csv(csv_path, index_to_plot, has_header=False):
    """
    Plots the values of a specified index across all rows in a single CSV file.

    Parameters:
    - csv_path (str): Path to the CSV file.
    - index_to_plot (int): The index (1-based) of the vector to plot.
    - has_header (bool): Whether the CSV file has a header row.
    """
    # Check if the file exists
    if not os.path.isfile(csv_path):
        print(f"Error: The file '{csv_path}' does not exist.")
        return

    try:
        # Read the CSV file
        if has_header:
            df = pd.read_csv(csv_path)
            total_columns = df.shape[1]
            selected_column = df.iloc[:, index_to_plot - 1]
            plt.xlabel('Row Number')
            plt.ylabel(f'Value at Index {index_to_plot}')
            title = f'Values at Index {index_to_plot} Across Rows in {os.path.basename(csv_path)}'
        else:
            df = pd.read_csv(csv_path, header=None)
            total_columns = df.shape[1]
            selected_column = df.iloc[:, index_to_plot - 1]
            plt.xlabel('Row Number')
            plt.ylabel(f'Value at Index {index_to_plot}')
            title = f'Values at Index {index_to_plot} Across Rows in {os.path.basename(csv_path)}'

        # Validate index_to_plot
        if index_to_plot < 1 or index_to_plot > total_columns:
            print(f"Error: index_to_plot should be between 1 and {total_columns}.")
            return

        # Inspect data around potential spike
        # For example, print the first 10 and last 10 values
        print("\nFirst 10 values at the specified index:")
        print(selected_column.head(10))
        print("\nLast 10 values at the specified index:")
        print(selected_column.tail(10))

        # Additionally, identify and print any unusually large values
        mean_val = selected_column.mean()
        std_val = selected_column.std()
        threshold = mean_val + 3 * std_val  # Define a threshold for outliers

        outliers = selected_column[selected_column > threshold]
        if not outliers.empty:
            print("\nPotential outliers detected:")
            print(outliers)
        else:
            print("\nNo potential outliers detected.")

        # Prepare the x-axis: row numbers starting from 1
        x_values = range(1, len(selected_column) + 1)

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(x_values, selected_column, marker='o', linestyle='-', color='b', label=f'Index {index_to_plot}')

        # Highlight outliers
        if not outliers.empty:
            plt.scatter(outliers.index + 1, outliers, color='r', label='Outliers')

        # Customize the plot
        plt.title(title)
        plt.grid(True)
        plt.legend()

        # Optionally, set x-ticks for better readability
        if len(x_values) <= 20:
            plt.xticks(x_values)  # Show all x-ticks if there are 20 or fewer
        else:
            # For many rows, set x-ticks at regular intervals
            interval = max(1, len(x_values) // 20)  # Aim for around 20 ticks
            plt.xticks(range(1, len(x_values) + 1, interval))

        plt.tight_layout()
        plt.show()

    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_path}' is empty.")
    except pd.errors.ParserError:
        print(f"Error: The file '{csv_path}' is malformed or cannot be parsed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # ==============================
    # Configuration Section
    # ==============================

    # Path to the CSV file you want to analyze
    csv_path = 'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\Logs\\Preference_vector_average.csv'  # Replace with your CSV file path

    # Specify whether your CSV has a header row
    has_header = True  # Set to True if your CSV has headers

    # Specify the index you want to plot (1-based indexing)
    index_to_plot = int(input('Index to plot?'))  # Example: Plot the 10th element in each row

    # ==============================
    # Execution Section
    # ==============================

    plot_vector_index_from_single_csv(csv_path, index_to_plot, has_header)

if __name__ == "__main__":
    main()
