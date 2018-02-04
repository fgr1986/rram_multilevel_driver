#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################
# v1.0, 1 nov 2017
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
import random

##############
# constants
##############
analog_mux_inputs = 16
generated_files_folder = "exported"
analog_mux_file = "analog_mux.va"
loads_subcircuit = "loads_subcircuit.scs"
tx_properties = "nch_mac l=tx_p_l w=tx_p_w m=1 nf=1"
# (source gate drain bulk)
# tx_0 (n_control_0 n_gate_loads 0 n_control_0) pch_mac ...

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
fl_analog_mux.write("module analog_mux(n_out, n_in);\n\n")
fl_analog_mux.write("\tparameter level=0;\n")
fl_analog_mux.write("\tinout n_in;\n")
fl_analog_mux.write("\telectrical n_in;\n")
fl_analog_mux.write("\tinout [" + str(analog_mux_inputs-1) + ":0] n_out;\n")
fl_analog_mux.write("\telectrical [" + str(analog_mux_inputs-1)
                    + ":0] n_out;\n")
fl_analog_mux.write("\tinteger select;\n")
fl_analog_mux.write("\tgenvar c;\n\n")
fl_analog_mux.write("\tanalog begin\n")
fl_analog_mux.write("\t\tselect = level;\n")
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
fl_loads_scs.write("// tx loads and analog_mux cell //\n")
fl_loads_scs.write("// v1.0 01/11/2017              //\n")
fl_loads_scs.write("//////////////////////////////////\n\n")

fl_loads_scs.write("subckt tx_loads (to_rram)\n\n")
# write
fl_loads_scs.write("\tparameters mux_level=0\n")
for i in range(analog_mux_inputs-1, 0, -1):
    # tx_0 (n_control_0 n_gate_loads 0 n_control_0)
    fl_loads_scs.write("\ttx_" + str(i) + " (n_control_" + str(i)
                       + " n_gate_loads"
                       + " n_control_" + str(i-1)
                       + " 0"
                       )
    fl_loads_scs.write(") " + tx_properties + "\n")
# last transistor
fl_loads_scs.write("\ttx_0 (n_control_0"
                   + " n_gate_loads"
                   + " 0"
                   + " 0"
                   )
fl_loads_scs.write(") " + tx_properties + "\n")
fl_loads_scs.write("\n\n\t// analog_mux connection\n\n")
# fl_loads_scs.write("\tm_0 (n_\<" + str(analog_mux_inputs-1)
#                    + "\:0\> to_rram)"
#                    + " analog_mux\n\n")
fl_loads_scs.write("\tm_0 (")

for i in range(analog_mux_inputs-1, -1, -1):
    fl_loads_scs.write("n_" + str(i) + " ")
    if((i % 10) == 0):
        fl_loads_scs.write("\n\t\t+ ")
fl_loads_scs.write(" to_rram) analog_mux level=mux_level\n\n")

fl_loads_scs.write("ends tx_loads\n")
# close file
fl_loads_scs.close()


print("done")
