import pandas as pd
import ast

# Load the data
df = pd.read_csv('ZPPG_performance_data.csv')

# Convert categorical columns to one-hot encoding
categorical_columns = ['Strange Smell?', 'Air Tastes Like', 'Feng Shui of Surrounding Area']
df = pd.get_dummies(df, columns=categorical_columns)

# Handle the 'Weird Sounds' column
# Convert the string representation of lists into actual lists
df['Weird Sounds'] = df['Weird Sounds'].apply(ast.literal_eval)

# Identify all unique sounds
unique_sounds = set()
for sounds in df['Weird Sounds']:
    unique_sounds.update(sounds)

# Create columns for each unique sound
for sound in unique_sounds:
    df[sound] = df['Weird Sounds'].apply(lambda x: sound in x)

# Drop the original 'Weird Sounds' column
df.drop('Weird Sounds', axis=1, inplace=True)

# Convert 'ZPPG Performance' from percentage to a float
df['ZPPG Performance'] = df['ZPPG Performance'].str.rstrip('%').astype('float') / 100.0

# Save the processed data to a new CSV file
df.to_csv('processed_ZPPG_performance_data.csv', index=False)
