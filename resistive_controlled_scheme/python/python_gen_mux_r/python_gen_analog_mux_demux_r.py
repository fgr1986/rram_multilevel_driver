#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################
# v1.0, 1 nov 2017
#######################

# Ejemplo:
# `include "constants.vams"
# `include "disciplines.vams"
# module analog_mux(n_out, n_in, v_sel);
# inout n_in;
# electrical n_in;
# inout [7:0] n_out;
# electrical [7:0] n_out;
# inout v_sel;
# electrical v_sel;
# integer select;
# genvar c;
# analog begin
# select = V(v_sel);
# in = V(n_in);
# generate c (0,7,1) begin
# if( c==select ) begin
# V(n_out[c], n_in) <+ 0;
# end else begin
# I(n_out[c], n_in) <+ 0;
# end
# end
# end
# endmodule


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
analog_mux_inputs = 512
generated_files_folder = "exported"
analog_mux_file = "analog_mux.va"
loads_subcircuit = "loads_subcircuit.scs"
resistor_properties = "resistor r=0.5k"
# "rppolywo_m lr=15.78u wr=2u multi=(1) m=1"

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
fl_loads_scs.write("// v0.1 24/10/2017              //\n")
fl_loads_scs.write("//////////////////////////////////\n\n")

fl_loads_scs.write("subckt resistive_loads (to_rram sel)\n\n")
# write
for i in range(analog_mux_inputs-1, 0, -1):
    fl_loads_scs.write("\tr_" + str(i) + " (n_" + str(i)
                       + " n_" + str(i-1)
                       + " 0) " + resistor_properties + "\n")
# last resistor
fl_loads_scs.write("\tr_0 (n_0 0 0) " + resistor_properties + " \n")
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
