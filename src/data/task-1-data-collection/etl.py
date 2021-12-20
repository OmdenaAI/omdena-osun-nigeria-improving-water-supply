import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sys


def load_data(dataset_filepath):
    """
    A function that loads the dataset into dataframe
    INPUT:
        dataset_filepath: -> Path to dataset
    OUTPUT:
        Returns the loaded dataframe
    """
    df = pd.read_csv(dataset_filepath, dtype='object')
    return df

def distance_between_two_points(lat1, lat2, lon1, lon2):

     """
     A procedure to get the distance between two points with latitdues and longitudes
     INPUTS:
        lat1: -> latitude of the first point in degree 
        lat2: -> latitude of the second point in degree 
        lon1: -> longitude of the first point in degree 
        lon2: -> longitude of the second point in degree 
     """    
    # The numpy module contains a function named
    # radians which converts from degrees to radians.

     #lon1a = np.radians(lon1)
    # lon2a = np.radians(lon2)
     lat1a = np.radians(lat1)
     lat2a = np.radians(lat2)
      
    # Haversine formula
    
     dlon = np.radians(lon2 - lon1)
     dlat = np.radians(lat2 - lat1)
     a = np.sin(dlat / 2)**2 + np.cos(lat1a) * np.cos(lat2a) * np.sin(dlon / 2)**2
 
    
     c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
     r = 6371
      
     # calculate the result

     return np.round(c * r, 6)


def clean_data_frame_step1(dataframe, state):
    """
    A procedure to clean the dataframe by selecting all the rows in a given state
    Columns with all NaN are dropped
    
    INPUTS:
        dataframe:-> the loaded dataframe to be cleansed
        state:> Nigerian state of interest e.g Osun, Lagos, Enugu, Kebbi etc
    OUTPUT:
        Returns:-> cleaned dataframe 
    """
    df= dataframe[dataframe['#adm1']==state]

    df.dropna(how='all', axis=1, inplace=True)

    
    # columns to drop
    cols_to_drop = ['row_id', '#source', '#facility_type', '#report_date', '#country_name', '#adm1', '#data_lnk', '#converted', '#country_id', '#install_year', 'created_timestamp', 'updated', 'public_data_source', 'water_tech_category', 'water_tech_original', 'count', 'management_original', 'public_data_source', 'clean_country_id', 'clean_country_name']
    df.drop(cols_to_drop, axis =1, inplace=True)

    return df



def clean_dataframe_step2(dataframe):
    """
    A procedure to further clean the dataframe
    Split the columns with '#' prefixes and drop the columns with # prefixes
    Calculate the distance_in_km using the earlier defined function
    Create the distance_in_km column
    Latitudes and longitudes are converted to float
    Columns with single values and others considered irrelevant columns 
    such as duplicated columns with slight differences  are dropped
    Create a hypothetical resident's latitude and longitude
    INPUT:
        dataframe:-> The returned dataframe cleaned in step1
    OUTPUT:
        Returns: -> Better cleansed dataframe
    """
    df = dataframe
    # columns with '#' prefixes
    cols_with_prefixes = ['#lat_deg', '#lon_deg', '#status_id', '#photo_lnk', '#water_source',
       '#water_source_clean', '#water_tech_clean', '#water_tech', '#adm2',
       '#management', '#pay', '#status', '#subjective_quality', '#notes']

    # Create new columns to replace columns with prefixes
    # Remove the # prefixes in some columns
    df['latitude'] = df['#lat_deg'].str.split('#',n= 1, expand=True)
    df['longitude'] = df['#lon_deg'].str.split('#',n= 1, expand=True)
    df['status_id'] = df['#status_id'].str.split('#',n= 1, expand=True)
    df['water_source'] = df['#water_source_clean'].str.split('#',n= 1, expand=True)
    df['water_tech_clean'] = df['#water_tech_clean'].str.split('#',n= 1, expand=True)
    df['water_tech'] = df['#water_tech'].str.split('#',n= 1, expand=True)
    df['adm2']    = df['#adm2'].str.split('#',n= 1, expand=True)
    df['management'] = df['#management'].str.split('#',n= 1, expand=True)
    df['pay'] = df['#pay'].str.split('#',n= 1, expand=True)
    df['status'] = df['#status'].str.split('#',n= 1, expand=True)
    df['subjective_quality'] = df['#subjective_quality'].str.split('#',n= 1, expand=True)
    df['water_point_location'] = df['#notes'].str.split('#',n= 1, expand=True)
    df['photo_link'] = df['#photo_lnk'].str.split('#', n=1, expand=True)

    df['#lat_deg'] = df['#lat_deg'].astype('float')
    df['#lon_deg'] = df['#lon_deg'].astype('float')

    # Create  hypothetical resident's latitude and longitude
    np.random.seed(0) 
    df.insert(0, 'resident_latitude', df['#lat_deg'] + 0.0051*np.random.rand(df.shape[0]))
    df.insert(1, 'resident_longitude', df['#lon_deg'] + 0.00982*np.random.rand(df.shape[0]))

    
    df.drop(cols_with_prefixes, axis=1, inplace=True)

    # Calculate the distance_in_km using the earlier defined function

    distance_in_km = []
    for row in df.itertuples(index=False):
        distance_in_km.append(
       distance_between_two_points(row.resident_latitude, row.latitude, row.resident_longitude, row.longitude)
       )

    df['distance_in_km'] = distance_in_km

    return df


def save_datafreame_in_database(df, database_filepath):
    # create an sqlite database engine using sqlalchemy
    engine = create_engine(f'sqlite:///{database_filepath}')
    # save the df in a table if exists replace
    df.to_sql('etlTable', engine, index=False, if_exists='replace')



def main():
    if len(sys.argv) == 4:

        dataset_filepath, state, database_filepath = sys.argv[1:]
        print('Loading data from: {}'.format(dataset_filepath))
        df1 = load_data(dataset_filepath)

        print('='*50)
        print("Step 1 of Data Cleaning...")
        df2= clean_data_frame_step1(df1, state)

        print("="*50)
        print("Step 2 of Data Cleaning...")
        df = clean_dataframe_step2(df2)

        print("="*50)
               
        
        print('Saving data ...\n  To   DATABASE: {}'.format(database_filepath))
        save_datafreame_in_database(df, database_filepath)
        
        
        print('='*50)
    
    else:
        print('Please provide the following parameters:\n '\
              'filepath of the dataset as the first argument\n'\
              'Nigerian state of interest as the second argument\n'\
              ' the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python task-1-data-collection/etl.py '\
              'task-1-data-collection/Water_Point_Data_Exchange__WPDx-Basic_.csv '\
              ' Osun '  ' task-1-data-collection/water-point.db')

    

if __name__ == '__main__':
    main()
