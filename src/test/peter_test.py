import numpy as np
import pandas as pd
import os

cwd = os.getcwd()
file_loc = os.path.abspath(__file__)
file_dir = os.path.dirname(file_loc)
os.chdir(file_dir)
test_file = "../../dataset/dataset/data/000/Trajectory/20081023025304.plt"

data = np.genfromtxt(test_file, names=['Latitude', 'Longitude', 'None', 'Altitude', 'Date_DS', 'Date', 'Time'], 
                     dtype=(float, float, int, int, float, str, str),
                                       delimiter=',', 
                                       skip_header=6
                                       )

data_2 = pd.read_csv(test_file, skiprows=6, header=None)

print(data[0])
print(data_2.head())