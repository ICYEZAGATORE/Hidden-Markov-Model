import pandas as pd
import os

# Path to your main folder containing all the recording folders
base_path = r"C:\Users\USER\Hidden-Markov-Model\Recordings"  # Change this

activities = ["Walking", "Jumping", "Standing", "Still"]

for activity in activities:
    accel_dfs = []
    gyro_dfs = []
    
    # Loop through all folders that start with the activity name
    for folder in sorted(os.listdir(base_path)):
        if folder.startswith(activity):
            folder_path = os.path.join(base_path, folder)
            
            accel_path = os.path.join(folder_path, "Accelerometer.csv")
            gyro_path = os.path.join(folder_path, "Gyroscope.csv")
            
            if os.path.exists(accel_path):
                accel_dfs.append(pd.read_csv(accel_path))
            if os.path.exists(gyro_path):
                gyro_dfs.append(pd.read_csv(gyro_path))
    
    # Combine all clips for this activity
    if accel_dfs:
        combined_accel = pd.concat(accel_dfs, ignore_index=True)
        combined_accel.to_csv(f"{activity}_accelerometer.csv", index=False)
        print(f"{activity} accelerometer: {len(combined_accel)} rows")
    
    if gyro_dfs:
        combined_gyro = pd.concat(gyro_dfs, ignore_index=True)
        combined_gyro.to_csv(f"{activity}_gyroscope.csv", index=False)
        print(f"{activity} gyroscope: {len(combined_gyro)} rows")

print("Done!")
