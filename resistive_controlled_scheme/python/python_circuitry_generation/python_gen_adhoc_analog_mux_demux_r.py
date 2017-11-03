#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################
# v1.0 1 nov 2017
#######################
#
# Similar to python_gen_analog_mux_demux_r.py
# But uses addhoc resistances read from import_data/files.csv
#
#######################

import glob
import os
import zipfile
# Regular Expressions
import re
# copy files
import shutil
# iterative file search
import fnmatch
# improved system calls
import subprocess

# improved system calls
import numpy as np


############################
# Parameters
############################
# To obtain the target resistances/resistive loads
# initial gaps defined in the netlists
initial_gaps = np.array([1.3e-9, 1.367e-9, 1.5e-9, 1.6e-9, 1.7e-9])
g_idx = 1
pre_min = '1t1r'
clip_r_read = True

##############
# Files/Folders
##############
# folders
if clip_r_read:
    generated_files_folder = 'exported_adhoc/clip_range_r_read'
else:
    generated_files_folder = 'exported_adhoc/full_range_r_read'
# files
analog_mux_file = pre_min + '_g_idx_' + str(g_idx) + '_analog_mux.va'
loads_subcircuit = pre_min + '_g_idx_' + str(g_idx) + '_loads_subcircuit.scs'
print('\n')
print('\t* Generating modules for ' + pre_min + ' cell, with gap: '
      + str(initial_gaps[g_idx]))
#import files
if clip_r_read:
    print('\t* Notice that r_read is constrained, not in the full range')
    data_file = 'import_data/clip_range_r_read/' + pre_min + '_ideal_load_resistances.csv'
else:
    data_file = 'import_data/full_range_r_read/' + pre_min + '_ideal_load_resistances.csv'

# resistor parameters
resistor_properties = 'resistor r='
resistor_3t = False
# "rppolywo_m lr=15.78u wr=2u multi=(1) m=1"
# resistor_3t = True

############################
# Import data
############################
full_data = np.genfromtxt(data_file, delimiter=',')
r_loads = full_data[:, g_idx]
analog_mux_inputs = r_loads.shape[0]
print('\t* Generating mux/loads for ' + str(analog_mux_inputs) + ' levels')

############################
# preparing folder
############################
# folder where python is executed
executing_path = os.path.abspath('.')
# create final folder
if not os.path.exists(generated_files_folder):
    os.makedirs(generated_files_folder)
# change folder
os.chdir(generated_files_folder)

############################
# exporting files
############################

# open analog_mux file
fl_analog_mux = open(analog_mux_file, 'w')

# write
fl_analog_mux.write('`include \"constants.vams\"\n')
fl_analog_mux.write('`include \"disciplines.vams\"\n\n')
fl_analog_mux.write('module analog_mux(n_out, n_in);\n\n')
fl_analog_mux.write('\t// optimized for ' +  pre_min + 'cell, \n')
fl_analog_mux.write('\t// inital gaps at ' + str(initial_gaps[g_idx]) + ' \n')
fl_analog_mux.write('\t// and ' + str(analog_mux_inputs) + ' levels \n\n')
fl_analog_mux.write('\tparameter level=0;\n')
fl_analog_mux.write('\tinout n_in;\n')
fl_analog_mux.write('\telectrical n_in;\n')
fl_analog_mux.write('\tinout [' + str(analog_mux_inputs-1) + ':0] n_out;\n')
fl_analog_mux.write('\telectrical [' + str(analog_mux_inputs-1)
                    + ':0] n_out;\n')
fl_analog_mux.write('\tinteger select;\n')
fl_analog_mux.write('\tgenvar c;\n\n')
fl_analog_mux.write('\tanalog begin\n')
fl_analog_mux.write('\t\tselect = level;\n')
fl_analog_mux.write('\t\tgenerate c (0,' + str(analog_mux_inputs-1)
                    + ',1) begin\n')
fl_analog_mux.write('\t\t\tif( c==select ) begin\n')
fl_analog_mux.write('\t\t\t\tV(n_out[c], n_in) <+ 0;\n')
fl_analog_mux.write('\t\t\tend else begin\n')
fl_analog_mux.write('\t\t\t\tI(n_out[c], n_in) <+ 0;\n')
fl_analog_mux.write('\t\t\tend\n')
fl_analog_mux.write('\t\tend\n')
fl_analog_mux.write('\tend\n')
fl_analog_mux.write('endmodule')
# close file
fl_analog_mux.close()

# aux file
fl_loads_scs = open(loads_subcircuit, 'w')

fl_loads_scs.write('simulator lang=spectre\n\n')
fl_loads_scs.write('ahdl_include \"' + analog_mux_file + '\"\n\n')
fl_loads_scs.write('//////////////////////////////////\n')
fl_loads_scs.write('// Resistive loads and analog_mux cell //\n')
fl_loads_scs.write('// v1.0 01/11/2017              //\n')
fl_loads_scs.write('//////////////////////////////////\n\n')

fl_loads_scs.write('subckt resistive_loads (to_rram)\n\n')
# write
fl_loads_scs.write('\t// optimized for ' +  pre_min + 'cell, \n')
fl_loads_scs.write('\t// inital gaps at ' + str(initial_gaps[g_idx]) + ' \n')
fl_loads_scs.write('\t// and ' + str(analog_mux_inputs) + ' levels \n\n')
fl_loads_scs.write("\tparameters mux_level=0\n")
for i in range(analog_mux_inputs-1, 0, -1):
    fl_loads_scs.write('\tr_' + str(i) + ' (n_' + str(i)
                       + ' n_' + str(i-1))

    # additional terminal
    if(resistor_3t):
        fl_loads_scs.write(' 0')
    fl_loads_scs.write(') ' + resistor_properties
                       + str(r_loads[i] - r_loads[i-1])
                       + '\n')
# first resistor
if(resistor_3t):
    fl_loads_scs.write('\tr_0 (n_0 0 0) '
                       + resistor_properties)
else:
    fl_loads_scs.write('\tr_0 (n_0 0) ' + resistor_properties)
fl_loads_scs.write(str(r_loads[0]) + '\n')
fl_loads_scs.write('\n\n\t// analog_mux connection\n\n')
# fl_loads_scs.write('\tm_0 (n_\<' + str(analog_mux_inputs-1)
#                    + '\:0\> to_rram sel)'
#                    + ' analog_mux\n\n')
fl_loads_scs.write('\tm_0 (')

for i in range(analog_mux_inputs-1, -1, -1):
    fl_loads_scs.write('n_' + str(i) + ' ')
    if((i % 10) == 0):
        fl_loads_scs.write('\n\t\t+ ')
fl_loads_scs.write(" to_rram) analog_mux level=mux_level\n\n")

fl_loads_scs.write('ends resistive_loads\n')
# close file
fl_loads_scs.close()


print('\n')
print('\tdone')
print('\n')
