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
MAX_ROW = 2500

def plt_to_df(file) -> pd.DataFrame:
    """
    Reads each activity entry up to 2500 points
    Drops irrelevant columns ----> Can be improved by only reading specific columns?
    returns dataframe. 
    """

    df = pd.read_csv(file, skiprows=6, header=None, nrows=MAX_ROW)
    df.columns = ['Latitude', 'Longitude', 'None', 'Altitude', 'Date_DS', 'Date', 'Time']
    df = df.drop['None', 'Date', 'Time']
    return df

def get_files_in_folder(directory_name: str) -> list:
    """
    Takes a directory_name, and returns a list of files in the folder.
    """
    folder_path = data_path + "/" + directory_name + "/Trajectory"
    files = os.listdir(folder_path)

    # removing any files that should not be there 
    files_filtered = [fnmatch.filter(file, '*.plt') for file in files]
    return files_filtered

def get_labels(directory_name) -> (bool, list):
    path = data_path + "/" + directory_name + "/labels.txt"
    # splits data based on space giving the following columns: 
    # date, clock_time, date, clock_time, transport_mode
    labels = np.genfromtxt(path, skip_header=1, dtype=str)
    print(labels[0:5])
    pass

if __name__ == '__main__':
    get_labels("010")