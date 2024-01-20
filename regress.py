import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler


trainfile = 'measured_train.csv'
testfile = 'measured_try.csv'
#testfile = 'cleared_sites_formated.csv'
known_perf = True
num_output = 15
min_good_mse = .0079



for runn in range(3):

    # Load the data
    existing_locations = pd.read_csv(trainfile)
    new_locations = pd.read_csv(testfile)

    # Check if 'Site_id' is in the dataframe's columns and rename it to 'ZPPG_id'
    if 'Site_id' in existing_locations.columns:
        existing_locations.rename(columns={'Site_id': 'ZPPG_id'}, inplace=True)
    if 'Site_id' in new_locations.columns:
        new_locations.rename(columns={'Site_id': 'ZPPG_id'}, inplace=True)


    '''
    cols_to_drop_pot = ['Longitude','Latitude',
                        'Shortitude','Deltitude',
                        'Feng_Shui_of_Surrounding_Area', # always drop?
                        'Local_Value_of_Pi',
                        'Murphys_Constant',  # never drop. 
                        'Strange_Smell_EXTREMELY',
                        'Strange_Smell_No', # always drop?
                        'Strange_Smell_Somewhat',
                        'Air_Tastes_Like_Apples',
                        'Air_Tastes_Like_Burning',
                        'Air_Tastes_Like_Copper','Air_Tastes_Like_Mint',
                        'Air_Tastes_Like_Nothing_In_Particular',
                        'Otherworldly_Skittering','Unearthly_Squelching',
                        'Eerie_Silence',  # always drop?
                        'Impossible_Humming','Unnatural_Buzzing'
                        ]
    
    numeric_cols = ['Longitude','Latitude','Shortitude','Deltitude','Feng_Shui_of_Surrounding_Area','Local_Value_of_Pi','Murphys_Constant']



    #always_drop = ['Eerie_Silence', 'Feng_Shui_of_Surrounding_Area', 'Air_Tastes_Like_Copper']
    always_drop = []

    #always_double = ['Murphys_Constant', 'Local_Value_of_Pi']
    always_double = []



    #always_cube = ['Murphys_Constant', 'Local_Value_of_Pi'] #,'Feng_Shui_of_Surrounding_Area' ]
    always_cube = []
    always_cube = ['Murphys_Constant']


    num_to_cube = random.randint(0, 3)
    random.shuffle(numeric_cols)
    cols_to_cube = numeric_cols[:num_to_cube] + always_cube


    

    num_to_double = random.randint(0, 5)
    if num_to_double == 5:
        num_to_double = 0
    if num_to_double >= 3:
        num_to_double = num_to_double + random.randint(0, 4)
    # shuffle cols_to_drop_pot
    random.shuffle(cols_to_drop_pot)
    # pick num_to_drop from cols_to_drop_pot
    cols_to_double = cols_to_drop_pot[:num_to_double] + always_double




    num_to_drop = random.randint(0, 6)
    if num_to_drop == 5:
        num_to_drop = 0
    if num_to_drop >= 4:
        num_to_drop = num_to_drop + random.randint(0, 9)
    # shuffle cols_to_drop_pot
    random.shuffle(cols_to_drop_pot)
    # pick num_to_drop from cols_to_drop_pot
    cols_to_drop = cols_to_drop_pot[:num_to_drop] + always_drop
    '''



    cols_to_drop=['Feng_Shui_of_Surrounding_Area']
    cols_to_double=['Deltitude', 'Local_Value_of_Pi','Eerie_Silence', 'Feng_Shui_of_Surrounding_Area', 'Latitude', 'Strange_Smell_EXTREMELY', 'Strange_Smell_No', 'Unearthly_Squelching', 'Unnatural_Buzzing']
    cols_to_cube=[ 'Murphys_Constant']


    for col in cols_to_cube:
        existing_locations[col] = existing_locations[col] ** 3
        new_locations[col] = new_locations[col] ** 3


    for col in cols_to_double:
        existing_locations[col] = existing_locations[col] * 2
        new_locations[col] = new_locations[col] * 2



    existing_drops = ['ZPPG_id', 'ZPPG_Performance'] + cols_to_drop
    # Separating features and target variable
    X = existing_locations.drop(existing_drops, axis=1)
    y = existing_locations['ZPPG_Performance']

    # Data normalization

    #scaler = StandardScaler()
    # or try...
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    # or...
    #from sklearn.preprocessing import RobustScaler
    #scaler = RobustScaler()


    X_scaled = scaler.fit_transform(X)

    # Train-test split for model validation
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    #X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)

    # Model training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Model evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)


    new_to_drop = ['ZPPG_id'] + cols_to_drop
    # Predicting for new locations
    new_locations_scaled = scaler.transform(new_locations.drop(new_to_drop, axis=1))
    new_locations['ZPPG_pred'] = model.predict(new_locations_scaled)




    # Selecting the top locations
    top_locations = new_locations.nlargest(num_output, 'ZPPG_pred')



    if known_perf:
        # Load the test_1.csv file
        test_1 = pd.read_csv('test_1.csv')

        # Merge the two DataFrames on the 'ZPPG_id' column
        merged_df = pd.merge(top_locations, test_1, left_on='ZPPG_id', right_on='ZPPG_ID')

        # Select and rename the desired columns
        output_df = merged_df[['ZPPG_id', 'ZPPG_pred', 'measured_ZPPG_Performance', 'RANK']]
        output_df.columns = ['ZPPG_id', 'ZPPG_pred', 'ZPPG_meas', 'Rank_meas']

    else:
        # Select and rename the desired columns
        output_df = top_locations[['ZPPG_id', 'ZPPG_pred']]
        output_df.columns = ['ZPPG_id', 'ZPPG_pred']

    # Create a copy of the DataFrame before modifying it
    output_df = output_df.copy()
    output_df.loc[:, 'Rank_pred'] = output_df['ZPPG_pred'].rank(ascending=False).astype(int)

    #print(f"Mean Squared Error: {mse}")


    if known_perf:
        if (output_df['Rank_meas'].head(12).mean() < 99.8) and (mse < min_good_mse):
            #if (output_df['Rank_meas'].head(12).mean() < 13.8) and (mse < .0095):  
            # Print the DataFrame without the index
            print(output_df.to_string(index=False))


            print("\n\n")
            print(f"Mean Squared Error: {mse}")

            # print ("average rank_meas of the top 12")
            print ("avg rank_meas of the top 12: \t", output_df['Rank_meas'].head(12).mean())
            print ("max rank_meas of the top 12: \t", output_df['Rank_meas'].head(12).max())
            print ("med rank_meas of the top 12: \t", output_df['Rank_meas'].head(12).median())


            cols_to_drop.sort()
            print(f"{cols_to_drop=}")

            cols_to_double.sort()
            print(f"{cols_to_double=}")

            cols_to_cube.sort()
            print(f"{cols_to_cube=}")

            quit()

        else:
            print(f"{runn=}   \t {mse=}")
    else:
        # print the top 12 ZPPG_id
        print(output_df['ZPPG_id'].head(12).to_string(index=False))

        print(output_df.to_string(index=False))
        print("\n\n")
        print(f"Mean Squared Error: {mse}")


        



