import re

def clean_servo_data(data):
    # Define regex patterns for splitting and replacing
    dimension_pattern = r'\?'
    torque_speed_pattern = r'(\d+\.\d+V)�(\d+\.\d+.*)'
    
    # Clean each entry
    cleaned_data = []
    for entry in data:
        # Split the entry into individual fields
        fields = entry.split(',')

        # Clean the Dimensions field
        if '?' in fields[4]:
            dimensions = fields[4].split(dimension_pattern)
            # Safely assign dimensions, filling missing values with empty strings
            fields[4] = dimensions[0] if len(dimensions) > 0 else ''
            fields[5] = dimensions[1] if len(dimensions) > 1 else ''
            fields[6] = dimensions[2] if len(dimensions) > 2 else ''
        else:
            # If no ? was found, assume single dimension and fill the rest with empty strings
            fields[5] = ''
            fields[6] = ''

        # Clean Torque and Speed fields
        torque_speed_matches = re.findall(torque_speed_pattern, fields[5])
        if torque_speed_matches:
            fields[7] = torque_speed_matches[0][0]  # Voltage
            fields[8] = torque_speed_matches[0][1]  # Torque
            if len(fields) > 6:
                torque_speed_matches = re.findall(torque_speed_pattern, fields[6])
                fields[9] = torque_speed_matches[0][0]  # Voltage for speed
                fields[10] = torque_speed_matches[0][1]  # Speed

        # Fill missing fields with empty strings
        fields = fields + [''] * (16 - len(fields))
        
        # Reorganize fields for output
        new_entry = [
            fields[0],  # Make
            fields[1],  # Model
            fields[2],  # Modulation
            fields[3],  # Weight
            fields[4],  # DimensionsL
            fields[5],  # DimensionsW
            fields[6],  # DimensionsH
            fields[7],  # TorqueV
            fields[8],  # TorqueOzIn
            fields[9],  # SpeedV
            fields[10], # Speed-s60
            fields[11], # Motor
            fields[12], # Rotation
            fields[13], # Gear
            fields[14], # Typical
            fields[15]  # Compare
        ]

        # Add cleaned entry to the list
        cleaned_data.append(','.join(new_entry))
    
    return cleaned_data

# Example raw data
raw_data = [
    "Ace RC,C0915,Analog,0.32 oz,0.87?0.45?0.93 in,4.8V�20.8 oz-in,4.8V�0.10 s/60�,(add),Single Bearing,Plastic,$30.99 ,",
    ",,,,,6.0V�26.4 oz-in,6.0V�0.08 s/60�,,,,,",
    "Ace RC,C1016,Analog,0.32 oz,0.87?0.45?0.93 in,4.8V�22.2 oz-in,4.8V�0.10 s/60�,(add),Single Bearing,Metal,$17.99 ,"
    # Add more entries as needed
]

# Clean the data
cleaned_data = clean_servo_data(raw_data)

# Output cleaned data
for entry in cleaned_data:
    print(entry)
