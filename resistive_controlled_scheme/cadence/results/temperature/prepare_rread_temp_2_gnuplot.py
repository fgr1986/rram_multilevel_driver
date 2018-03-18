import numpy as np


file_path = './rread_temperature.csv'
export_path ='processed.csv'


# data = np.loadtxt(file_path, delimiter=',', unpack=True)
data = np.genfromtxt(file_path, delimiter=',', skip_header=False)[:,:]
print(data.shape)
time = data[:, 0]
filtered_data = data[:, 1::2]
print(filtered_data.shape)

f_data = np.zeros([filtered_data.shape[0], filtered_data.shape[1]+1])
f_data[:,0] = time
f_data[:, 1:] = filtered_data

print(f_data.shape)
np.savetxt(export_path, f_data, delimiter=',')
