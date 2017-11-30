remove spureous data


# if exported from viva:
# first row: headers
# (maybe inbetween rows)
# second/last row: data in X0 Y0, X1, Y1 format, grab all Y values
last_r_read = np.array([full_data[full_data.shape[0]-1, 1::2]])
r_length = int(last_r_read.shape[1]/n_gaps)
last_r_read = last_r_read.reshape(n_gaps, r_length)
print(last_r_read[5, 1:].shape)
for r_idx, r in enumerate(last_r_read[5, 1:]):
    a_idx = r_idx + 1
    if r < last_r_read[5, a_idx-1]:
        print(a_idx)
        print(r_loads[a_idx])
        print('updated ' + str(last_r_read[5, a_idx]) + ' +1=' + str(last_r_read[5, a_idx+1]) + ' -1=' + str(last_r_read[5, a_idx-1]))
        last_r_read[5, a_idx] = (last_r_read[5, a_idx+1]+last_r_read[5, a_idx-1])/2
        print('by ' + str(last_r_read[5, a_idx]))
np.savetxt("/home/fgarcia/Desktop/1t1r.data",
           last_r_read, delimiter=",")
