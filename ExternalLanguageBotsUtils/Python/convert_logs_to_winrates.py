import csv
import tensorflow as tf
import os

def csv_to_tensorboard_log(csv_file, log_dir, split_logs=False):
    # Ensure the log directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        writer = None
        current_file_index = 0
        
        # Iterate over the rows in the CSV file
        for row in reader:
            step = int(row['Step'])
            value = float(row['Value'])
            
            # Create a new log file for every 'split_logs' steps or for every row if split_logs is True
            if split_logs and (writer is None or step % split_logs == 0):
                if writer is not None:
                    writer.close()
                writer = tf.summary.create_file_writer(os.path.join(log_dir, f"PPO_{current_file_index}"))
            
            # Write the scalar value to the TensorBoard log
            with writer.as_default():
                tf.summary.scalar('Value', value, step=step)
                writer.flush()

        # Ensure the last writer is closed
        if writer is not None:
            writer.close()

    print(f"TensorBoard logs have been written to {log_dir}")

# Example usage

csv_file = f'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\RESULTS\\PPO_V14_PPO_vs_itself_0.csv'  # Path to your CSV file
log_dir = f'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\RESULTS\\adjusted-logs\\PPO_V14\\PPO_vs_itself_0'  # Directory to save the TensorBoard logs
split_logs = 1  # Change this to the number of steps after which a new log file is created. Set to 1 for one log per row
csv_to_tensorboard_log(csv_file, log_dir, split_logs)


# Example usage