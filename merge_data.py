import pandas as pd
import os

# Path to your dataset folder
dataset_dir = "/Users/mac/formative 2/dataset"
final_data = []

# Loop through all the activity folders
for item in os.listdir(dataset_dir):
    folder_path = os.path.join(dataset_dir, item)
    
    if os.path.isdir(folder_path):
        # Extract the clean label (lower case, removing numbers and dates)
        label_part = item.split('-')[0]
        label = ''.join([i for i in label_part if not i.isdigit()]).lower()
        
        acc_path = os.path.join(folder_path, "Accelerometer.csv")
        gyro_path = os.path.join(folder_path, "Gyroscope.csv")
        
        # Only process if both files exist
        if os.path.exists(acc_path) and os.path.exists(gyro_path):
            try:
                # Load the data
                acc_df = pd.read_csv(acc_path)
                gyro_df = pd.read_csv(gyro_path)
                
                # Check if data exists in both
                if len(acc_df) == 0 or len(gyro_df) == 0:
                    print(f"⚠️ Empty files found in {item}, skipping.")
                    continue
                
                # Rename columns
                acc_df = acc_df.rename(columns={'x': 'acc_x', 'y': 'acc_y', 'z': 'acc_z'})
                gyro_df = gyro_df.rename(columns={'x': 'gyro_x', 'y': 'gyro_y', 'z': 'gyro_z'})
                
                # Merge based on timestamp (nearest match)
                acc_df = acc_df.sort_values('seconds_elapsed')
                gyro_df = gyro_df.sort_values('seconds_elapsed')
                merged_df = pd.merge_asof(acc_df, gyro_df, on='seconds_elapsed', direction='nearest')
                
                # Add labels to tell us which recording this is
                merged_df['Activity'] = label
                merged_df['Session_ID'] = item  # Keep original folder name just in case
                
                # Drop extra time columns from the merge if they persist, keeping seconds_elapsed
                if 'time_x' in merged_df.columns:
                    merged_df = merged_df.drop(columns=['time_x'])
                if 'time_y' in merged_df.columns:
                    merged_df = merged_df.drop(columns=['time_y'])
                if 'time' in merged_df.columns:
                    merged_df = merged_df.drop(columns=['time'])
                
                # Keep only necessary columns
                cols = ['seconds_elapsed', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'Activity', 'Session_ID']
                merged_df = merged_df[cols]
                
                final_data.append(merged_df)
                print(f"✅ Successfully processed {item} (Label: {label})")
            except Exception as e:
                print(f"❌ Error processing {item}: {e}")

# Combine everything into one giant dataframe
if final_data:
    final_df = pd.concat(final_data, ignore_index=True)
    # Save it!
    output_path = "/Users/mac/formative 2/merged_sensor_data.csv"
    final_df.to_csv(output_path, index=False)
    print(f"\n🎉 Done! Saved final dataset of {len(final_df)} rows to: {output_path}")
    
    # Print a summary of counts by activity
    print("\nData distribution by Activity:")
    print(final_df['Activity'].value_counts())
else:
    print("No data found to process.")
