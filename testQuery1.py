import pandas as pd
import re
# Load the CSV data
df = pd.read_csv('servoTestFile.csv')

# Function to split rows with multiple Torque and Speed entries
def split_rows(row):
    torque_values = re.findall(r'(\d+\.\d+V\s[\d\.]+\s\w+-in)', row['Torque'])
    speed_values = re.findall(r'(\d+\.\d+V\s[\d\.]+\ss/60°)', row['Speed'])
    
    # Ensure that the lengths match
    if len(torque_values) != len(speed_values):
        raise ValueError("Mismatch between the number of Torque and Speed entries.")
    
    # Generate new rows
    new_rows = []
    for i in range(0, len(torque_values), 2):
        new_row = row.copy()
        new_row['Torque'] = ' '.join(torque_values[i:i+2])
        new_row['Speed'] = ' '.join(speed_values[i:i+2])
        new_rows.append(new_row)
    
    return new_rows

# Apply the function to rows where there's more than one Torque and Speed entry
expanded_rows = []
for _, row in df.iterrows():
    if len(row['Torque'].split(' ')) > 2:  # Assuming the data is split with spaces
        expanded_rows.extend(split_rows(row))
    else:
        expanded_rows.append(row)

# Create a new DataFrame from the expanded rows
cleaned_df = pd.DataFrame(expanded_rows)

# Save the cleaned DataFrame to a new CSV file
cleaned_df.to_csv('cleaned_file.csv', index=False)
