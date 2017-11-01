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

##############
# constants
##############
generated_files_folder = "exported_adhoc"
analog_mux_file = "analog_mux.va"
loads_subcircuit = "loads_subcircuit.scs"

############################
# Parameters
############################
# To obtain the target resistances/resistive loads
# initial gaps defined in the netlists
initial_gaps = np.array([1.3e-9, 1.367e-9, 1.5e-9, 1.6e-9, 1.7e-9])
# data from ../stand_alone_simulations/resistive_controlled_scheme/results
print('Printing data for every gap in ' + str(initial_gaps))
pre = 'exported_results/1t1r_'
g_idx = 0
pre_min = '1t1r'
data_file = 'import_data/' + pre_min + '_ideal_load_resistances.csv'
resistor_properties = "resistor r="
# "rppolywo_m lr=15.78u wr=2u multi=(1) m=1"

############################
# Import data
############################
full_data = np.genfromtxt(data_file, delimiter=',')
r_loads = full_data[:, g_idx]
analog_mux_inputs = r_loads.shape[0]
print("generating mux/loads for " + str(analog_mux_inputs) + " levels")

############################
# preparing folder
############################
# folder where python is executed
executing_path = os.path.abspath(".")
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
fl_analog_mux.write("`include \"constants.vams\"\n")
fl_analog_mux.write("`include \"disciplines.vams\"\n\n")
fl_analog_mux.write("module analog_mux(n_out, n_in, v_sel);\n\n")
fl_analog_mux.write("\tinout n_in;\n")
fl_analog_mux.write("\telectrical n_in;\n")
fl_analog_mux.write("\tinout [" + str(analog_mux_inputs-1) + ":0] n_out;\n")
fl_analog_mux.write("\telectrical [" + str(analog_mux_inputs-1)
                    + ":0] n_out;\n")
fl_analog_mux.write("\tinout v_sel;\n")
fl_analog_mux.write("\telectrical v_sel;\n\n")
fl_analog_mux.write("\tinteger select;\n")
fl_analog_mux.write("\tgenvar c;\n\n")
fl_analog_mux.write("\tanalog begin\n")
fl_analog_mux.write("\t\tselect = V(v_sel);\n")
fl_analog_mux.write("\t\tgenerate c (0," + str(analog_mux_inputs-1)
                    + ",1) begin\n")
fl_analog_mux.write("\t\t\tif( c==select ) begin\n")
fl_analog_mux.write("\t\t\t\tV(n_out[c], n_in) <+ 0;\n")
fl_analog_mux.write("\t\t\tend else begin\n")
fl_analog_mux.write("\t\t\t\tI(n_out[c], n_in) <+ 0;\n")
fl_analog_mux.write("\t\t\tend\n")
fl_analog_mux.write("\t\tend\n")
fl_analog_mux.write("\tend\n")
fl_analog_mux.write("endmodule")
# close file
fl_analog_mux.close()

# aux file
fl_loads_scs = open(loads_subcircuit, 'w')

fl_loads_scs.write("simulator lang=spectre\n\n")
fl_loads_scs.write("ahdl_include \"" + analog_mux_file + "\"\n\n")
fl_loads_scs.write("//////////////////////////////////\n")
fl_loads_scs.write("// Resistive loads and analog_mux cell //\n")
fl_loads_scs.write("// v1.0 01/11/2017              //\n")
fl_loads_scs.write("//////////////////////////////////\n\n")

fl_loads_scs.write("subckt resistive_loads (to_rram sel)\n\n")
# write
for i in range(analog_mux_inputs-1, 0, -1):
    fl_loads_scs.write("\tr_" + str(i) + " (n_" + str(i)
                       + " n_" + str(i-1)
                       + " 0) " + resistor_properties
                       + str(r_loads[i] - r_loads[i-1])
                       + "\n")
# first resistor
fl_loads_scs.write("\tr_0 (n_0 0 0) "
                   + resistor_properties
                   + str(r_loads[0])
                   + "\n")
fl_loads_scs.write("\n\n\t// analog_mux connection\n\n")
# fl_loads_scs.write("\tm_0 (n_\<" + str(analog_mux_inputs-1)
#                    + "\:0\> to_rram sel)"
#                    + " analog_mux\n\n")
fl_loads_scs.write("\tm_0 (")

for i in range(analog_mux_inputs-1, -1, -1):
    fl_loads_scs.write("n_" + str(i) + " ")
    if((i % 10) == 0):
        fl_loads_scs.write("\n\t\t+ ")
fl_loads_scs.write(" to_rram sel) analog_mux\n\n")

fl_loads_scs.write("ends resistive_loads\n")
# close file
fl_loads_scs.close()


print("done")
