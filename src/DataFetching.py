"""
File: DataFetching.py
Date: 29.09.2023
Description: Fetches data from 
"""
import os
from itertools import filterfalse
import fnmatch
import pandas as pd
import numpy as np
from typing import List

data_path = "../dataset/Data"

#--------------Classes---------------------#

class Activity: 

    def __init__(self, user: str, trackpoints_path: str) -> None:
        self.start = None
        self.end = None
        self.user = user
        self.trackpoints = trackpoints_path
        self.transport_m = None
    
    def get_track_points(self) -> (bool, pd.DataFrame):
        """
        Returns dataframe with plotpoints but also sets start_time and end_time of activity
        """
        try: 
            df = plt_to_df(self.trackpoints)
            time = df['Date_DS'].apply(ole_to_datetime)  
            datetime = pd.to_datetime(time, unit='ms')
            df['datetime'] = datetime
            df = df.drop(columns=['Date_DS'])

            self.start = df['datetime'].iloc[0]
            self.end = df['datetime'].iloc[-1]
            if len(df) > 2500: 
                return False, df
            else: 
                return True, df
        except Exception as e: 
            print("Exception in get_track_points function:\n ", e)
            raise Exception(e)

# -------------Functions-------------------#
def plt_to_df(file) -> pd.DataFrame:
    """
    Reads each activity entry up to 2500 points
    Drops irrelevant columns ----> Can be improved by only reading specific columns?
    returns dataframe. 
    """

    df = pd.read_csv(file, skiprows=6, header=None)
    df.columns = ['Latitude', 'Longitude', 'None', 'Altitude', 'Date_DS', 'Date', 'Time']
    df = df.drop(columns=['None', 'Date', 'Time'])
    return df

def get_files_in_folder(directory_name: str) -> list:
    """
    Takes a directory_name, and returns a list of files in the folder.
    """
    try: 
        return os.listdir(directory_name) 
    except Exception as e: 
        print(directory_name)
        return e

def get_plt_files(user_name: str) -> list: 
    """
    Filters out .plt files for a given user
    """
    folder_path = data_path + "/" + user_name + "/Trajectory"
    files =  get_files_in_folder(folder_path)
    # removing any files that should not be there 
    files_filtered = fnmatch.filter(files, '*.plt')
    return files_filtered

def get_users():
    return get_files_in_folder(data_path)

def get_labels(user_name) -> pd.DataFrame:
    path = data_path + "/" + user_name + "/labels.txt"
    # splits data based on space giving the following columns: 
    # date, clock_time, date, clock_time, transport_mode
    try:
        labels = np.genfromtxt(path, skip_header=1, dtype=str)
        
        
        df = pd.DataFrame(labels, columns=['start_time', 
                                        'start_clock', 
                                        'end_time', 
                                        'end_clock', 
                                        'transportation_mode']
                                        )
        df = time_and_date_to_datetime(df)
        return df
    except Exception as e:
        print("Something bad happened here in get_labels() ", e)
        exit()

def get_activities(user: str) -> List[Activity]:
    files = get_plt_files(user)
    activities: list[Activity] = []
    for file in files:
        path = data_path + "/" + user + "/Trajectory/" + file
        activities.append(Activity(user, path))
    return activities

def time_and_date_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    start = pd.to_datetime(df['start_time'] + " " + df['start_clock'])
    end = pd.to_datetime(df['end_time'] + " " + df['end_clock'])
    df['start_date_time'] = start
    df['end_date_time'] = end
    return(df.drop(columns=['start_time', 'start_clock', 'end_time', 'end_clock']))

def ole_to_datetime(ole: float) -> float:
    unix = (ole - 25569) * 24 * 3600 * 1000
    return unix

## primarily used for testing
if __name__ == '__main__':
    activities = get_activities('010')
    points = activities[0].get_track_points()
    a = activities[0]
    
    print(f'User: {a.user}    start: {a.start}    end: {a.end}    path: {a.trackpoints}')
    
    