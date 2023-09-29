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

data_path = "../dataset/Data"


def plt_to_df(file) -> pd.DataFrame:
    """
    Reads each activity entry up to 2500 points
    Drops irrelevant columns ----> Can be improved by only reading specific columns?
    returns dataframe. 
    """

    df = pd.read_csv(file, skiprows=6, header=None)
    df.columns = ['Latitude', 'Longitude', 'None', 'Altitude', 'Date_DS', 'Date', 'Time']
    df = df.drop['None', 'Date', 'Time']
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
        return pd.DataFrame(labels, columns=['start_time', 
                                        'start_clock', 
                                        'end_time', 
                                        'end_clock', 
                                        'transportation_mode']
                                        )
    except Exception as e:
        print("Something bad happened here in get_labels() ", e)
        exit()
    

if __name__ == '__main__':
    #print(get_labels("010"))
    print(get_plt_files("010"))
    print(get_users())
    