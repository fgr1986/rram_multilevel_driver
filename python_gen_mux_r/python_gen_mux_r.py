#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################
# v0.4 6 feb 2017
#######################

# Ejemplo:
# module mux(v_in, v_out, v_sel);
#   output v_out;
#   electrical v_out;
#   input [1:0] v_in;
#   input v_sel;
#   electrical [1:0] v_in;
#   electrical v_sel ;
#   // parameter integer sel = 0;
#   integer select;
#   real in;
#   analog begin
#     select = V(v_sel);
#     case (select)
#       0:        in=V(v_in[0]);
#       1:        in=V(v_in[1]);
#       default:  in=0;
#     endcase
#     V(v_out) <+ in;
#   end
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
mux_inputs = 8
generated_files_folder = "exported"
mux_file = "mux.va"
loads_subcircuit = "loads_subcircuit.scs"
resistor_properties = "rppolywo_m lr=15.78u wr=2u multi=(1) m=1"

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

# open mux file
fl_mux = open(mux_file, 'w')

# write
fl_mux.write("`include \"constants.vams\"\n")
fl_mux.write("`include \"disciplines.vams\"\n\n")
fl_mux.write("module mux(v_in, v_out, v_sel);\n\n")
fl_mux.write("\tinout v_out;\n")
fl_mux.write("\telectrical v_out;\n\n")
fl_mux.write("\tinout [" + str(mux_inputs-1) + ":0] v_in;\n")
fl_mux.write("\tinout v_sel;\n")
fl_mux.write("\telectrical [" + str(mux_inputs-1) + ":0] v_in;\n")
fl_mux.write("\telectrical v_sel;\n\n")
fl_mux.write("\tinteger select;\n")
fl_mux.write("\treal in;\n\n")
fl_mux.write("\tanalog begin\n\n")

fl_mux.write("\t\tselect = V(v_sel);\n")

fl_mux.write("\t\tcase (select)\n")
for i in range(0, mux_inputs):
    fl_mux.write("\t\t\t" + str(i) + ":        in=V(v_in[" + str(i) + "]);\n")
fl_mux.write("\t\t\tdefault:  in=0;\n")
fl_mux.write("\t\tendcase\n")

fl_mux.write("\t\tV(v_out) <+ in;\n\n")
fl_mux.write("\t\tend\n")
fl_mux.write("\tendmodule\n")

# close file
fl_mux.close()

# aux file
fl_loads_scs = open(loads_subcircuit, 'w')

fl_loads_scs.write("simulator lang=spectre\n\n")
fl_loads_scs.write("ahdl_include \"" + mux_file + "\"\n\n")
fl_loads_scs.write("//////////////////////////////////\n")
fl_loads_scs.write("// Resistive loads and mux cell //\n")
fl_loads_scs.write("// v0.1 24/10/2017              //\n")
fl_loads_scs.write("//////////////////////////////////\n\n")

fl_loads_scs.write("subckt resistive_loads (to_rram sel)\n\n")
# write
for i in range(mux_inputs-1, 0, -1):
    fl_loads_scs.write("\tr_" + str(i) + " (n_" + str(i)
                       + " n_" + str(i-1)
                       + " 0) " + resistor_properties + "\n")
# last resistor
fl_loads_scs.write("\tr_0 (n_0 0 0) " + resistor_properties + " \n")
fl_loads_scs.write("\n\n\t// mux connection\n\n")
# fl_loads_scs.write("\tm_0 (n_\<" + str(mux_inputs-1) + "\:0\> to_rram sel)"
#                    + " mux\n\n")
fl_loads_scs.write("\tm_0 (")

for i in range(mux_inputs-1, -1, -1):
    fl_loads_scs.write("n_" + str(i) + " ")
    if((i % 10) == 0):
        fl_loads_scs.write("\n\t\t+ ")
fl_loads_scs.write(" to_rram sel) mux\n\n")

fl_loads_scs.write("ends resistive_loads\n")
# close file
fl_loads_scs.close()


print("done")
