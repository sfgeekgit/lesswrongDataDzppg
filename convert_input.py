import pandas as pd
import ast

#input_file = 'ZPPG_performance_data.csv'
#output_file = 'measured_data.csv'

input_file = 'cleared_sites_data.csv'
output_file = 'cleared_sites_formated.csv'

has_perf = False
remove_id = False

# Load the data
df = pd.read_csv(input_file)

# Convert categorical columns to one-hot encoding
categorical_columns = ['Strange Smell?', 'Air Tastes Like']
df = pd.get_dummies(df, columns=categorical_columns)

# Handle the 'Weird Sounds' column
# Convert the string representation of lists into actual lists
df['Weird Sounds'] = df['Weird Sounds'].apply(ast.literal_eval)

unique_sounds = set()
for sounds in df['Weird Sounds']:
    unique_sounds.update(sounds)
for sound in unique_sounds:
    df[sound] = df['Weird Sounds'].apply(lambda x: sound in x).astype(float)


df.drop('Weird Sounds', axis=1, inplace=True) # Drop the original 'Weird Sounds' column

feng_shui_mapping = {'Disharmonious': 0, 'Adequate': 0.5, 'Exceptional': 1}
df['Feng Shui of Surrounding Area'] = df['Feng Shui of Surrounding Area'].map(feng_shui_mapping)

if has_perf:
    # Convert 'ZPPG Performance' from percentage to a float
    df['ZPPG Performance'] = df['ZPPG Performance'].str.rstrip('%').astype('float') / 100.0


if remove_id:
    # Drop the 'ZPPG id' column
    df.drop('ZPPG id', axis=1, inplace=True)

# Identify the new column names after one-hot encoding
cols_to_convert = [col for col in df.columns if 'Strange Smell' in col or 'Air Tastes Like' in col]

# Convert each column to float and rename it
for col in cols_to_convert:
    df[col] = df[col].astype(float)
    df.rename(columns={col: col.replace(' ', '_').replace('?', '')}, inplace=True)

# Replace all spaces in all column names with underscores
df.columns = df.columns.str.replace(' ', '_')
# remove all ' from column names
df.columns = df.columns.str.replace('\'', '')


# List of column names in the desired order
cols_order = ['ZPPG_id', 'Longitude', 'Latitude', 'Shortitude', 'Deltitude', 'Feng_Shui_of_Surrounding_Area', 'Local_Value_of_Pi', 'Murphys_Constant', 'Strange_Smell_EXTREMELY', 'Strange_Smell_No', 'Strange_Smell_Somewhat', 'Air_Tastes_Like_Apples', 'Air_Tastes_Like_Burning', 'Air_Tastes_Like_Copper', 'Air_Tastes_Like_Mint', 'Air_Tastes_Like_Nothing_In_Particular', 'Otherworldly_Skittering', 'Unearthly_Squelching', 'Eerie_Silence', 'Impossible_Humming', 'Unnatural_Buzzing', 'ZPPG_Performance']

# Check if the first column is 'ZPPG_id' or 'Site_id'
if 'Site_id' in df.columns:
    cols_order[0] = 'Site_id'

# Check if 'ZPPG_Performance' should be included
if not has_perf:
    cols_order.remove('ZPPG_Performance')

# Reorder the columns
df = df[cols_order]

# Save the processed data to a new CSV file
df.to_csv(output_file, index=False)
